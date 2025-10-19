import os
import pandas as pd
import parallel_logos as download_module
import image_similarity as similarity_module

FILE_PATH = "logos.snappy.parquet"
DISTANCE_THRESHOLD = 9 
LOGOS_FOLDER = "logos"
GROUPED_FOLDER = "grouped_logos"

def main():
    try:
        df = pd.read_parquet(FILE_PATH)
        domains = df["domain"].tolist()
        print(f"Found {len(domains)} domains")
    except FileNotFoundError:
        print(f"ERROR: {FILE_PATH} not found")
        return

    download_module.download_logos(domains)

    if not os.path.exists(LOGOS_FOLDER) or not os.listdir(LOGOS_FOLDER):
        print("ERROR: No logos found")
        return

    print("Generating phashes...")
    file_phash_map = similarity_module.phash_generator()

    if not file_phash_map:
        print("ERROR: No phashes generated")
        return

    file_paths = list(file_phash_map.keys())

    print("Generating distance matrix...")
    distance_matrix = similarity_module.build_distances_matrix(file_phash_map)

    print("Clustering...")
    clustering_labels = similarity_module.agglomerativeClustering(distance_matrix, DISTANCE_THRESHOLD)
    
    print("Grouping...")
    similarity_module.group(file_paths, clustering_labels)

    print("FINISHED")
    
if __name__ == "__main__":
    main()