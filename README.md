# Veridion-Challenge

This project implements a robust, two-stage pipeline to download company logos from a domain list and automatically group them based on visual similarity. The main goal is to efficiently identify various versions or duplicates of the same brand logo within a large dataset.

1. Architecture and Execution Flow

The project is structured into two separate modules, each for a specific type of computational task (I/O or CPU). The entire process is orchestrated by the main.py script.
Module              Primary Task	            Optimization Technique	            Core Technologies
parallel_logos.py	Logo Download (I/O-Bound)	Multithreading (ThreadPoolExecutor)	requests, Logo.dev API
image_similarity.py	Logo Clustering (CPU-Bound)	Clustering Algorithms	            imagehash, scikit-learn, NumPy

Pipeline Stages:

    Read Domains: Reads company domains from the .parquet file.

    Parallel Download: Multithreading is used to fetch all logo images concurrently.

    Hashing: Calculates the Perceptual Hash (pHash) for each downloaded image.

    Distance Matrix: Calculates the Hamming Distance between all possible logo pairs (the most CPU-intensive step).

    Clustering: Applies Agglomerative Clustering to assign similarity labels.

    Grouping: Copies files into organized sub-folders named grouped_logos/group_[ID].

2. Technical Solution Details

2.1. Efficient Data Acquisition

    External API for Logos: Logo assets are sourced directly using the Logo.dev API, which is a highly reliable third-party service for retrieving high-quality logos based on a company's domain. This strategy avoids the complexity, instability and maintenance overhead associated with direct web scraping.

    Concurrency for I/O: The download process is inherently I/O-bound (waiting for network responses). Multithreading (ThreadPoolExecutor with 30 workers) is utilized to ensure the Python script does not wait idly; instead, it concurrently manages multiple active network requests.

2.2. Similarity Clustering

To accurately group logos regardless of minor changes (compression, size, or background color), the system relies on Perceptual Hashing rather than traditional pixel comparison.

    Feature Extraction (pHash): The Perceptual Hash (pHash) algorithm from the imagehash library is used to generate a unique digital fingerprint (a hash) that represents the visual structure of the logo.

    Distance Metric: Similitude is measured using the Hamming Distance between two hashes. A low Hamming Distance (e.g. 0-9) implies high visual similarity.

    Clustering Algorithm: AgglomerativeClustering (scikit-learn) is applied:

        It uses the pre-calculated Distance Matrix (metric='precomputed') as input.

        It defines a similarity threshold (distance_threshold=9) to determine the maximum acceptable difference for two logos to belong to the same group.

3. Usage and Setup

Dependencies

Install the required libraries:
Bash

pip3 install pandas requests pillow imagehash numpy scipy scikit-learn

Execution

Run the complete pipeline from the project root directory:
Bash

python3 main.py

4. Suggested Future Improvements

To enhance the project's performance, robustness and independence, the following improvements are recommended:

4.1. CPU Optimization (Matrix Calculation)

The step that calculates the Hamming Distance Matrix is the most CPU-intensive (O(N2)).

    Action: Transition the build_distances_matrix function from the current sequential for loop to use ProcessPoolExecutor (Multiprocessing). This will allow the calculation to utilize all available CPU cores simultaneously, drastically reducing execution time for large datasets.

4.2. Logo Extraction Robustness

Relying solely on a third-party API introduces a single point of failure (API outage, service discontinuation).

    Action: Implement a Fallback/Primary Scraping Mechanism. If the external API fails to return a logo, the program should fall back to direct inspection of the company's homepage. This involves:

        Making a requests.get() to the company domain.

        Using Beautiful Soup to search the HTML for high-confidence logo indicators, such as:

            <meta property="og:image">

            <link rel="icon"> or <link rel="apple-touch-icon">

            <img> tags with class="logo" or id="brand".

5. Thinking Process: From Concept to Solution

When I initially approached this challenge, the overall complexity felt daunting and I struggled to define a clear endpoint. My strategy quickly shifted to an iterative, step-by-step approach: even without knowing the final destination, I focused on identifying the immediate next step.

5.1. Resource Understanding and Initial Strategy

The first action was a thorough investigation of the available resources. I analyzed the contents of the .parquet file to understand its data structure, confirming it was populated with numerous domain URLs.

This clarity immediately defined the primary goal: Resource Gathering. The next step was clearly to find the corresponding company logos for each domain.

My initial idea was to perform a GET request to each domain’s homepage and parse the returned HTML. I quickly identified several complexities with this scraping approach:

    Non-Standardization: Logos could be located in various HTML elements (meta tags, <link>, <img> tags with unique classes).

    Ambiguity: Multiple images on a single page could be easily confused with the official logo.

    Normalization Overhead: Successful extraction would require subsequent steps to standardize resolution, format (e.g. converting SVG to PNG/JPG) and filename, which felt overly tedious.

5.2. Adoption of External APIs (Efficiency Pivot)

Recognizing the overhead of building a robust scraping and normalization service, I pivoted to searching for specialized third-party solutions. I discovered two professional logo APIs: Logo.clearbit and Logo.dev. Given that Clearbit's service was scheduled for discontinuation, Logo.dev became the preferred choice, allowing for highly efficient and standardized logo retrieval.

5.3. Optimizing Resource Gathering (Concurrency)

With the resource gathering logic defined, the immediate next problem became performance. A sequential download approach, waiting for each server response individually, would take an unacceptable amount of time.

    Decision: I recognized that the download stage was I/O-bound (network limited). To overcome this bottleneck, I implemented multithreading using Python's ThreadPoolExecutor. This strategy allowed the program to manage multiple download requests concurrently, significantly improving performance and reducing the total execution time.

5.4. Feature Engineering for Similarity (Clustering)

With the complete set of logos efficiently gathered, I moved to the second major stage: clustering. The goal was to group logos based on visual resemblance, which required a simplified, robust image representation.

    Feature Choice: I discovered Perceptual Hashing (pHash) and the Hamming Distance as the ideal solution. After reviewing explanatory videos, I understood that pHash could convert complex visual data into a compact binary string that captures the image's structural fingerprint, making the comparison resilient to noise and minor compression changes.

    Implementation: I proceeded with the implementation using specialized Python tools (imagehash, scikit-learn, NumPy) to calculate the full distance matrix and apply Agglomerative Clustering, defining a clear, data-driven threshold for visual similarity.