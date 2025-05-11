import os
import pandas as pd
import streamlit as st
import re
from runners.segmenting import seg_slices, display_slices, kmean_seg
from runners.control_injured import run_model
# from runners.fibrosis_classification import unsupervised_clustering


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

seg_bool = False


with home:
    file_path = "markdown_files/homepage.md"
    with open(file_path, "r", encoding="utf-8") as file:
        content = file.read()
    st.markdown(content, unsafe_allow_html=True)

with ml:
    st.markdown("## **Machine Learning**")

    seg = st.file_uploader("Upload a .nii or .nii.gz", type=["nii", "nii.gz", "gz"])

    if seg and not(seg_bool):
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

        # if predicted[0] == "Injured":
        #     my_dict = unsupervised_clustering()
        #     display_slices(r'user_slices/kmean_segmentation')
        #     cluster_df = pd.DataFrame.from_dict(my_dict)
        #     cluster_df.columns = ["Image", "Cluster"]
        #     # st.dataframe(cluster_df)
        #     st.markdown(f"#### User Image classified in Cluster {cluster_df.loc[cluster_df['Image'] == 'user_slices/kmean_segmentation', 'Cluster'].iloc[0]}")
        #     st.markdown("Cluster 0 typically has less dark green and I believe it has a lesser degree of capsule fibrosis.")
        #     st.markdown("Cluster 1 typically has more dark green and I believe it has a higher degree of capsule fibrosis.")
        #     st.markdown("I have not encountered a Cluster 2, but I would guess that it has a higher degree than Cluster 1.")

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

    image = st.file_uploader(
        "Upload a .nii or .nii.gz for segmentation", type=["nii", "nii.gz", "gz"]
    )

    if image:
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