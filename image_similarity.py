import os
from PIL import Image
import imagehash
import numpy as np
from scipy.spatial.distance import squareform
from sklearn.cluster import AgglomerativeClustering
import shutil

logos_folder = "logos"

file_phash_map = {}

for image in os.listdir(logos_folder):
    image_path = os.path.join(logos_folder, image)

    if os.path.isdir(image_path):
        continue

    file_phash_map[image_path] = imagehash.phash(Image.open(image_path))

file_paths = list(file_phash_map.keys())
phashes = list(file_phash_map.values())
n = len(phashes)
distances = []

for i in range(n):
    for j in range(i + 1, n):
        distances.append(phashes[i] - phashes[j])

print("Done building distances matrix")

distance_matrix = squareform(np.array(distances))
distance_threshold = 9

clustering = AgglomerativeClustering(n_clusters=None, distance_threshold=distance_threshold, metric='precomputed', linkage='average')
clustering_labels = clustering.fit_predict(distance_matrix)

grouped_folder = "grouped_logos"
os.makedirs(grouped_folder, exist_ok=True)

for i, id in enumerate(clustering_labels):
    file_name = file_paths[i]
    group_folder_name = f"group_{id}"
    dest = os.path.join(grouped_folder, group_folder_name)
    src = file_name

    try:
        os.makedirs(dest, exist_ok=True)
        if (os.path.exists(src)):
            shutil.copy(src, dest)
            print(f"File {file_name} copied to {dest}")
    except Exception as e:
        print(f"Error at file {file_name}: {e}")
