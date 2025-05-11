## https://colab.research.google.com/drive/1GloftmUEYIWMv_ROJnQzBsVz2zYBk_Wn?authuser=2#scrollTo=3ANWuC4nHUx6

import os
import torch
import torch.nn as nn
from monai.networks.nets import UNet
from monai.transforms import LoadImaged, DivisiblePad
import numpy as np
from PIL import Image
from skimage.transform import resize
import matplotlib.pyplot as plt
import streamlit as st
import nibabel as nib
import cv2
from sklearn.cluster import KMeans


class UNet3DWithSelectiveDropout(nn.Module):
    def __init__(self, in_channels=1, out_channels=1, features=(32, 64, 128, 64), dropout1=0.2, dropout2=0.2):
        super(UNet3DWithSelectiveDropout, self).__init__()

        # Define MONAI's UNet
        self.unet = UNet(
            spatial_dims=3,
            in_channels=in_channels,
            out_channels=out_channels,
            channels=features,
            strides=(2, 2, 2),
            num_res_units=2,
            act=("LeakyReLU", {"negative_slope": 0.01, "inplace": True}),
            norm=("batch", {"eps": 1e-5, "momentum": 0.1}),
            dropout=0  # Disable built-in dropout
        )

        # Dropout layers
        self.dropout_after_second_layer = nn.Dropout3d(p=dropout1)
        self.dropout_after_fourth_layer = nn.Dropout3d(p=dropout2)

    def forward(self, x):
        x = self.unet.model[0](x)  # Initial convolution

        # Apply dropout selectively during forward pass
        for i, layer in enumerate(self.unet.model[1:]):
            x = layer(x)
            if i == 2:  # Apply dropout after the 2nd layer
                x = self.dropout_after_second_layer(x)
            if i == 4:  # Apply dropout after the 4th layer
                x = self.dropout_after_fourth_layer(x)

        return x


class UNet3DWithSelectiveDropout2(nn.Module):
    def __init__(self, in_channels=1, out_channels=1, features=(32, 64, 128, 256), dropout1=0.2, dropout2=0.2):
        super(UNet3DWithSelectiveDropout2, self).__init__()

        # Define MONAI's UNet
        self.unet = UNet(
            spatial_dims=3,
            in_channels=in_channels,
            out_channels=out_channels,
            channels=features,
            strides=(2, 2, 2),
            num_res_units=2,
            act=("LeakyReLU", {"negative_slope": 0.01, "inplace": True}),
            norm=("batch", {"eps": 1e-5, "momentum": 0.1}),
            dropout=0  # Disable built-in dropout
        )

        # Dropout layers
        self.dropout_after_second_layer = nn.Dropout3d(p=dropout1)
        self.dropout_after_fourth_layer = nn.Dropout3d(p=dropout2)

    def forward(self, x):
        x = self.unet.model[0](x)  # Initial convolution

        # Apply dropout selectively during forward pass
        for i, layer in enumerate(self.unet.model[1:]):
            x = layer(x)
            if i == 2:  # Apply dropout after the 2nd layer
                x = self.dropout_after_second_layer(x)
            if i == 4:  # Apply dropout after the 4th layer
                x = self.dropout_after_fourth_layer(x)

        return x


@st.cache_resource()
def make_model():
    """
    loads in models for use by segmentation and seg_slice
    """
    device = torch.device("cpu")
    model = UNet3DWithSelectiveDropout(in_channels=1, out_channels=1).to(device)
    model.load_state_dict(torch.load("models/unet_3d_elbow_segmentation-875.pth", map_location=torch.device("cpu")))
    model_seg = UNet3DWithSelectiveDropout2(in_channels=1, out_channels=1).to(device)
    model_seg.load_state_dict(torch.load("models/unet_3d_elbow_segmentation-35.pth", map_location=torch.device("cpu")))

    return [model, model_seg]

@st.cache_resource()
def make_kmeans():
    cluster_centers = np.load("models/cluster_centers.npy")
    return KMeans(n_clusters=6, random_state=42, init=cluster_centers, n_init=1)


def kmean_seg(mri_path):
    """
    used for getting kmeans segmentaion when loading in
    .nii or .nii.gz in machine learning tab or segmentation tab
    it will be used for unsupervised clustering
    """
    # Step 1: Load NIfTI file
    mask_path = "user_slices/masks/user_image.nii.gz"
    os.makedirs("user_slices/kmean_segmentation", exist_ok=True)
    kmeans = make_kmeans()

    # Load NIfTI image (you can replace the path with your own)
    def load_nii(file_path):
        nii_img = nib.load(file_path)
        return nii_img.get_fdata()  # Convert to NumPy array

    image = load_nii(mri_path)
    mask = load_nii(mask_path)


    # Resize mask
    mask_resized = np.array([cv2.resize(mask[:, :, i], (image.shape[1], image.shape[0]), interpolation=cv2.INTER_NEAREST)
                            for i in range(image.shape[2])]).transpose(1, 2, 0)

    # Normalize image
    image_normalized = (image - np.min(image)) / (np.max(image) - np.min(image))

    # Apply mask
    image_masked = image_normalized * mask_resized

    # Reshape for classification
    valid_pixels = image_masked[image_masked > 0].reshape(-1, 1)

    # Perform K-Means clustering on all valid pixels
    labels = kmeans.fit_predict(valid_pixels)

    # Reconstruct clustered image
    clustered_image = np.zeros(image_masked.shape, dtype=np.int32)
    valid_pixel_indices = image_masked > 0
    clustered_image[valid_pixel_indices] = labels

    # Define distinct colors for each cluster
    cluster_colors = np.array([
        [42, 157, 143],  # 🌿 Teal (#2a9d8f)
        [231, 111, 81],  # 🎀 Salmon Pink (#e76f51)
        [135, 191, 255], # 🔹 Sky Blue (#87BFFF)
        [38, 70, 83],    # 🌊 Deep Blue (#264653)
        [233, 196, 106], # 🍂 Mustard Yellow (#e9c46a)
        [162, 155, 254]  # 🍇 Soft Purple (#a29bfe)
    ], dtype=np.uint8)

    # Select 16 evenly spaced slices
    axis = 2
    num_slices = 16
    indices = np.linspace(0, clustered_image.shape[axis] - 1, num_slices, dtype=int)

    # Save selected slices
    for idx, i in enumerate(indices):
        slice_data = np.take(clustered_image, i, axis=axis)

        # Map cluster labels to RGB colors
        slice_colored = cluster_colors[slice_data]

        # Convert to RGB image
        img = Image.fromarray(slice_colored, mode="RGB")

        # Save only middle slices
        if 7 < idx < 12:
            img.save(f"user_slices/kmean_segmentation/user_image_{idx-7}.png")
        elif idx >= 12:
            break

def seg_slices(mri_path):
    """
    used for getting full and partial segmentation
    when loading in .nii or .nii.gz in machine learning tab
    to be used for control_injured
    """
    device = torch.device("cpu")
    # Define the base directory
    base_dir = "user_slices"

    # Ensure the top-level directories exist for MRI, partial_seg, and full_seg
    folders = {
        "MRI": os.path.join(base_dir, "mri_slices"),
        "Partial_Seg": os.path.join(base_dir, "partial_segmentation"),
        "Full_Seg": os.path.join(base_dir, "full_segmentation")
    }
    the_model = make_model()
    model = the_model[0]
    model_seg = the_model[1]
    model.eval()
    model_seg.eval()

    def normalize_slice(slice_data):
        """Normalize MRI slice to 0-255 and convert to uint8."""
        slice_data = (slice_data - np.min(slice_data)) / (np.max(slice_data) - np.min(slice_data)) * 255.0
        return slice_data.astype(np.uint8)

    def overlay_segmentation(mri_slice, seg_mask):
        """Overlay segmentation mask (red) on MRI slice, ensuring they match in size."""
        # Normalize MRI slice to 0-255 and convert to uint8
        mri_slice = normalize_slice(mri_slice)

        # Resize segmentation mask to match the MRI slice shape
        seg_mask_resized = resize(seg_mask, mri_slice.shape, mode='constant', anti_aliasing=True)

        # Binarize and scale the segmentation mask
        seg_mask_resized = (seg_mask_resized > 0.5).astype(np.uint8) * 255

        # Convert grayscale to RGB (using 3 channels for MRI)
        mri_colored = np.stack([mri_slice] * 3, axis=-1)
        mri_colored[..., 0] = np.maximum(mri_colored[..., 0], seg_mask_resized)  # Apply red mask

        return Image.fromarray(mri_colored)

    # Load MRI
    loader = LoadImaged(keys=["image"])
    mri_dict = loader({"image": mri_path})
    mri = mri_dict["image"]

    # Normalize MRI
    mri = (mri - mri.min()) / (mri.max() - mri.min())

    # Pad to be divisible by 16
    div_transform = DivisiblePad(k=16)
    mri_tensor = div_transform(mri.as_tensor().float().unsqueeze(0))  # Shape: (1, D, H, W)
    mri_tensor = mri_tensor.unsqueeze(0).to(device)  # Shape: (1, 1, D, H, W)

    with torch.no_grad():
        partial_seg = torch.sigmoid(model(mri_tensor)).cpu().numpy().squeeze()
        full_seg = torch.sigmoid(model_seg(mri_tensor)).cpu().numpy().squeeze()
        partial_seg = (partial_seg > 0.875).astype(np.float32)  # Apply threshold for partial_seg
        full_seg = (full_seg > 0.35).astype(np.float32)  # Apply threshold for full_seg

    # Convert PyTorch tensor to NumPy array
    seg_output_np = full_seg.squeeze()
    # Load the original NIfTI file to get the affine
    mri_nib = nib.load(mri_path)

    # Save the segmentation output as a NIfTI file
    seg_nii = nib.Nifti1Image(seg_output_np, affine=mri_nib.affine)
    nib.save(seg_nii, "user_slices/masks/user_image.nii.gz")

    # Extract slices (7,8,9,10 out of 16)
    num_slices = 16
    axis = 2  # Assuming depth axis
    slice_indices = np.linspace(0, mri.shape[axis] - 1, num_slices, dtype=int)[7:11]
    name = "user_image"
    for idx, i in enumerate(slice_indices):
        # Extract slices
        mri_slice = np.take(mri, i, axis=axis)
        partial_seg_slice = np.take(partial_seg, i, axis=axis)
        full_seg_slice = np.take(full_seg, i, axis=axis)

        # Convert and save MRI slice
        img_mri = Image.fromarray(normalize_slice(mri_slice))
        img_mri.save(os.path.join(folders["MRI"], f"{name}_{idx}.png"))

        # Convert and save segmentation overlay images
        img_partial_seg = overlay_segmentation(mri_slice, partial_seg_slice)
        img_partial_seg.save(os.path.join(folders["Partial_Seg"], f"{name}_{idx}.png"))

        img_full_seg = overlay_segmentation(mri_slice, full_seg_slice)
        img_full_seg.save(os.path.join(folders["Full_Seg"], f"{name}_{idx}.png"))


def display_slices(path):
    """
    will display full_segmentation slices on screen with
    regular mri slices
    """
    images = sorted([os.path.join(path, f) for f in os.listdir(path) if f.endswith('.png')])
    for i, col in enumerate(st.columns(4)):
        with col:
            image = Image.open(images[i])

            # Create a new figure to avoid overlapping plots
            fig, ax = plt.subplots()
            ax.imshow(image)
            ax.axis("off")  # Hide axes for better visualization

            # Display image in Streamlit
            st.pyplot(fig)