## https://colab.research.google.com/drive/1X3jlo5y8P3pjwPj_vK07-5nQKcTe-5n1?authuser=2#scrollTo=QgxQSJK0JY_E
import os
import numpy as np
import torchvision.models as models
from torch.utils.data import Dataset, DataLoader
import torch.nn.functional as F
import torch
import torch.nn as nn
from torchvision import transforms
# from torchvision.models import EfficientNet_B0_Weights
import streamlit as st
from PIL import Image

class ElbowDataset(Dataset):
    """
    sets dataset for mean image and the control vs injured ml model
    """
    def __init__(self, root_dir, transform=None):
        self.root_dir = root_dir
        self.transform = transform
        self.samples = []

        images = sorted([os.path.join(root_dir, f) for f in os.listdir(root_dir) if f.endswith('.png')])
        if len(images) != 0:
            self.samples.append((images, "user_image"))
        

    def __len__(self):
        return len(self.samples)

    def __getitem__(self, idx):
        image_paths, label = self.samples[idx]  # Get list of 4 image paths and label

        images = []
        for image_path in image_paths:
            if os.path.exists(image_path):
                image = Image.open(image_path).convert("RGB")  # Load image in RGB format

                if self.transform:
                    image = self.transform(image)

                images.append(image)

        images = torch.stack(images)  # Shape: (4, 3, 224, 224)

        # Compute mean image representation (reduce the 4 images into one)
        images = images.mean(dim=0)  # Shape now becomes (3, 224, 224)

        return images, torch.tensor(0 if label == "Control" else 1)  # 0 = control, 1 = injured


device = torch.device("cuda" if torch.cuda.is_available() else "cpu")


@st.cache_resource()
def get_model():
    """
    Establishes categorical model for injury vs control.
    """
    model = models.efficientnet_b0(weights=True)
    num_features = model.classifier[1].in_features
    model.classifier[1] = nn.Linear(num_features, 2)  # 2 classes
    model.load_state_dict(torch.load("models/model_state_full.pth"))
    # Move model to the appropriate device
    model.to(device)  # This line is CRUCIAL

    return model




def run_model(folder_dir):
    """
    Runs categorical model for injury vs control and returns the predicted label with confidence.
    """
    model = get_model()
    model.eval()

    transform = transforms.Compose([
        transforms.Resize((480, 480)),  # Match EfficientNet input size
        transforms.RandomHorizontalFlip(p=0.5),  # Introduce variability while preserving key features
        transforms.RandomRotation(degrees=10),  # Small rotation to preserve anatomical structures
        transforms.RandomResizedCrop(224, scale=(0.9, 1.0)),  # Less aggressive cropping to retain ROI
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.5], std=[0.5])  # Adjust normalization if grayscale MRI (single channel)
    ])

    test_dataset = ElbowDataset(folder_dir, transform=transform)
    test_loader = DataLoader(test_dataset, batch_size=1)  # Ensure single input at a time

    with torch.no_grad():
        for inputs, labels in test_loader:  # Get inputs and labels
            inputs, labels = inputs.to(device), labels.to(device)  # Move to correct device

            outputs = model(inputs)  # Raw logits
            probabilities = F.softmax(outputs, dim=1)  # Convert to probabilities
            confidence, predicted = torch.max(probabilities, 1)

            return ("Injured" if predicted.item() == 1 else "Control"), np.round(confidence.item() * 100, 2)  # Return label & confidence percentage

    return None, None  # Return None if no data is processed


