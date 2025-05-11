import os
import pandas as pd
import streamlit as st
import re
from runners.segmenting import seg_slices, display_slices, kmean_seg
from runners.control_injured import run_model
from runners.fibrosis_classification import unsupervised_clustering


st.set_page_config(page_title="Bio-Mechanical", layout="wide")

st.markdown("# DSS-Bio-Mechanical")

home, ml, segmentation, appendix = st.tabs(
    [
        "Home",
        "Machine Learning",
        "Segmentation",
        "Appendix",
    ]
)


ml_files = [None, "C053L", "C054L", "6012", "6013", "6139", "6140", "6315", "6342R", "6344R"]
labels = [None, "Control", "Control", "Injured", "Injured", "Injured", "Injured", "Injured", "Injured", "Injured"]

ml_locations_full = [
    None,
    "full_segmentation/Control/C053L",
    "full_segmentation/Control/C054L",
    "full_segmentation/Injured/6012",
    "full_segmentation/Injured/6013",
    "full_segmentation/Injured/6139",
    "full_segmentation/Injured/6140",
    "full_segmentation/Injured/6315",
    "full_segmentation/Injured/6342R",
    "full_segmentation/Injured/6344R",
]
ml_locations_part = [
    None,
    "partial_segmentation/Control/C053L",
    "partial_segmentation/Control/C054L",
    "partial_segmentation/Injured/6012",
    "partial_segmentation/Injured/6013",
    "partial_segmentation/Injured/6139",
    "partial_segmentation/Injured/6140",
    "partial_segmentation/Injured/6315",
    "partial_segmentation/Injured/6342R",
    "partial_segmentation/Injured/6344R",
]
ml_locations_kmean = [
    None,
    "kmean_segmentation/Control/C053L",
    "kmean_segmentation/Control/C054L",
    "kmean_segmentation/Injured/6012",
    "kmean_segmentation/Injured/6013",
    "kmean_segmentation/Injured/6139",
    "kmean_segmentation/Injured/6140",
    "kmean_segmentation/Injured/6315",
    "kmean_segmentation/Injured/6342R",
    "kmean_segmentation/Injured/6344R",
]


seg_files = [None, "C052L", "6342L", "6127L", "6126L", "6342R", "6344R"]

seg_locations_full = [
    None,
    "full_segmentation/Control/C052L",
    "full_segmentation/Control/6342L",
    "full_segmentation/Injured/6127L",
    "full_segmentation/Injured/6126L",
    "full_segmentation/Injured/6342R",
    "full_segmentation/Injured/6344R",
]
seg_locations_part = [
    None,
    "partial_segmentation/Control/C052L",
    "partial_segmentation/Control/6342L",
    "partial_segmentation/Injured/6127L",
    "partial_segmentation/Injured/6126L",
    "partial_segmentation/Injured/6342R",
    "partial_segmentation/Injured/6344R",
]
seg_locations_kmean = [
    None,
    "kmean_segmentation/Control/C052L",
    "kmean_segmentation/Control/6342L",
    "kmean_segmentation/Injured/6127L",
    "kmean_segmentation/Injured/6126L",
    "kmean_segmentation/Injured/6342R",
    "kmean_segmentation/Injured/6344R",
]
seg_bool = False


with home:
    file_path = "markdown_files/homepage.md"
    with open(file_path, "r", encoding="utf-8") as file:
        content = file.read()
    st.markdown(content, unsafe_allow_html=True)

with ml:
    st.markdown("## **Machine Learning**")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        file = st.selectbox("Test Images", options = ml_files, placeholder="Choose an option")

    seg = st.file_uploader("Upload a .nii or .nii.gz", type=["nii", "nii.gz", "gz"])

    if file and not(seg) and not(seg_bool):
        folder_dir = ml_files.index(file)
        predicted = run_model(ml_locations_full[folder_dir])

        st.markdown(f"#### Prediction: {predicted[0]} at {predicted[1]}% confidence")
        st.markdown(f"#### Actual Label {labels[folder_dir]}")

        display_slices(ml_locations_full[folder_dir])

        if predicted[0] == "Injured" and labels[folder_dir] == "Injured":
            my_dict = unsupervised_clustering()
            display_slices(ml_locations_kmean[folder_dir])
            cluster_df = pd.DataFrame.from_dict(my_dict)
            cluster_df.columns = ["Image", "Cluster"]
            cluster_df["Cluster"] = cluster_df["Cluster"].astype(int)
            st.markdown(f"#### Image {file} classified in Cluster {cluster_df.loc[cluster_df['Image'] == file, 'Cluster'].iloc[0]}")
            st.markdown("Cluster 0 typically has less dark green and I believe it is a lesser degree of capsule fibrosis.")
            st.markdown("Cluster 1 typically has more dark green and I believe it is a higher degree of capsule fibrosis.")
            st.markdown("I have not encountered a Cluster 2, but I would guess that it is a higher degree than Cluster 1.")


    elif seg and not(seg_bool):
        # Save the uploaded file if needed
        save_path = "user_slices/" + re.sub("^[^.]+", "user_image", seg.name)
        if os.path.exists(save_path):
            os.remove(save_path)

        with open(save_path, "wb") as f:
            f.write(seg.getbuffer())
        seg_bool = True

        seg_slices(save_path)
        kmean_seg(save_path)

        predicted = run_model("user_slices/full_segmentation")

        st.markdown(f"#### Prediction: {predicted[0]} at {predicted[1]}% confidence")

        display_slices("user_slices/full_segmentation")

        if predicted[0] == "Injured":
            my_dict = unsupervised_clustering()
            display_slices(r'user_slices/kmean_segmentation')
            cluster_df = pd.DataFrame.from_dict(my_dict)
            cluster_df.columns = ["Image", "Cluster"]
            # st.dataframe(cluster_df)
            st.markdown(f"#### User Image classified in Cluster {cluster_df.loc[cluster_df['Image'] == 'user_slices/kmean_segmentation', 'Cluster'].iloc[0]}")
            st.markdown("Cluster 0 typically has less dark green and I believe it has a lesser degree of capsule fibrosis.")
            st.markdown("Cluster 1 typically has more dark green and I believe it has a higher degree of capsule fibrosis.")
            st.markdown("I have not encountered a Cluster 2, but I would guess that it has a higher degree than Cluster 1.")

    if seg_bool:
        if os.path.exists("user_slices/user_image.nii"):
            os.remove("user_slices/user_image.nii")

        folders = [
            os.path.join("user_slices", f)
            for f in os.listdir("user_slices")
            if os.path.isdir(os.path.join("user_slices", f))
        ]
        for folder in folders:
            for path in os.listdir(folder):
                full_path = os.path.join(folder, path)
                if os.path.isfile(full_path):
                    os.remove(full_path)
        seg_bool = False


with segmentation:
    st.markdown("## **Segmentation**")
    col1, col2, col3 = st.columns(3)
    with col1:
        seg_file = st.selectbox("Test Images", options = seg_files, placeholder="Choose an option")

    image = st.file_uploader(
        "Upload a .nii or .nii.gz for segmentation", type=["nii", "nii.gz", "gz"]
    )
    if seg_file and not(image) and not(seg_bool):
        folder_dir = seg_files.index(seg_file)
        
        st.markdown("#### Full Segmentation")
        display_slices(seg_locations_full[folder_dir])

        st.markdown("#### Partial Segmentation")
        display_slices(seg_locations_part[folder_dir])

        st.markdown("#### Kmean Segmentation")
        display_slices(seg_locations_kmean[folder_dir])

    elif image:
        # Save the uploaded file if needed
        save_path = "user_slices/" + re.sub("^[^.]+", "user_image", image.name)
        if os.path.exists(save_path):
            os.remove(save_path)

        with open(save_path, "wb") as f:
            f.write(image.getbuffer())
        seg_bool = True

        seg_slices(save_path)
        kmean_seg(save_path)

        st.markdown("#### Full Segmentation")
        display_slices("user_slices/full_segmentation")

        st.markdown("#### Partial Segmentation")
        display_slices("user_slices/partial_segmentation")

        st.markdown("#### Kmean Segmentation")
        display_slices("user_slices/kmean_segmentation")

    if seg_bool:
        if os.path.exists("user_slices/user_image.nii"):
            os.remove("user_slices/user_image.nii")

        folders = [
            os.path.join("user_slices", f)
            for f in os.listdir("user_slices")
            if os.path.isdir(os.path.join("user_slices", f))
        ]
        for folder in folders:
            for path in os.listdir(folder):
                full_path = os.path.join(folder, path)
                if os.path.isfile(full_path):
                    os.remove(full_path)
        seg_bool = False

with appendix:
    file_path = "markdown_files/appendix.md"
    with open(file_path, "r", encoding="utf-8") as file:
        content = file.read()
    st.markdown(content, unsafe_allow_html=True)