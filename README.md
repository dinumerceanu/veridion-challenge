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
