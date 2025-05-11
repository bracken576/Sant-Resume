## https://colab.research.google.com/drive/1Tcc8GYIJHW4mfax833AoLDBjj2Su6c_v?authuser=2#scrollTo=GM9_rZ26Pq8w

import os
import numpy as np
from PIL import Image
from sklearn.cluster import SpectralClustering
from sklearn.decomposition import PCA
from sklearn.metrics import silhouette_score
from collections import Counter
import cv2
import streamlit as st

def unsupervised_clustering():
    """
    will use the kmean segmentations to 
    cluster the images.
    returns dictionary of images and cluster group
    """
    # Path to the 3D images (each has 4 slices)
    image_folder = r"kmean_segmentation/Injured"
    additional_folder = r"user_slices/kmean_segmentation"
    image_groups = {}
    for folder in os.listdir(image_folder):
        folder_path = os.path.join(image_folder, folder)
        slices = sorted(os.listdir(folder_path))  # Sort to maintain order
        image_groups[folder] = [os.path.join(folder_path, img) for img in slices]
    if len(os.listdir(additional_folder)) != 0:
        image_groups[additional_folder] = [os.path.join(additional_folder, img) for img in slices]

    # Feature extraction function using PIL
    def extract_features(image_path):
        try:
            image = Image.open(image_path).convert("RGB")  # Ensure RGB format
            image = image.resize((100, 100))  # Resize for consistency
            image = np.array(image)  # Convert to NumPy array
        except Exception as e:
            print(f"Error loading {image_path}: {e}")
            return np.zeros(512)  # Return a zero vector for missing images

        # Calculate histogram
        hist = cv2.calcHist([image], [0, 1, 2], None, [8, 8, 8], [0, 256, 0, 256, 0, 256])
        return hist.flatten()  # Convert to 1D feature vector

    # Process all images
    image_features = {}  # Store features per image

    for image_name, slices in image_groups.items():
        features = [extract_features(slice_file) for slice_file in slices]
        image_features[image_name] = np.array(features)  # Shape: (4, feature_dim)

    # Reduce dimensionality using PCA
    all_features = np.vstack(list(image_features.values()))  # Stack all images' slices together
    pca = PCA(n_components=20)
    all_features_pca = pca.fit_transform(all_features)

    # Split PCA-transformed features back into image groups
    split_features = {}
    start_idx = 0
    for image_name in image_groups.keys():
        split_features[image_name] = all_features_pca[start_idx:start_idx + 4]  # Get the 4 slices
        start_idx += 4

    # Try different cluster numbers and choose the best one
    best_n = 2  # Minimum number of clusters
    best_score = -1

    for n_clusters in range(2, 6):
        sc = SpectralClustering(n_clusters=n_clusters, affinity="nearest_neighbors", assign_labels="kmeans", random_state=42)
        labels = sc.fit_predict(all_features_pca)

        score = silhouette_score(all_features_pca, labels)  # Evaluate clustering quality
        print(f"Clusters: {n_clusters}, Silhouette Score: {score}")

        if score > best_score:
            best_score = score
            best_n = n_clusters
            best_labels = labels

    st.markdown(f"#### Best number of clusters: {best_n} with a Silhouette Score: {best_score:.2f}")

    # Assign cluster labels per 3D image
    image_cluster_labels = {}

    start_idx = 0
    for image_name, slices in image_groups.items():
        slice_labels = best_labels[start_idx:start_idx + 4]  # Get cluster labels for 4 slices
        consensus_label = Counter(slice_labels).most_common(1)[0][0]  # Majority voting
        image_cluster_labels[image_name] = consensus_label
        start_idx += 4

    # Print final image classification
    return image_cluster_labels.items()
        
