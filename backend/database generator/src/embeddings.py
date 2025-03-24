import torch
import numpy as np
from src.model_loader import load_model
from src.preprocess import preprocess_image, tokenize_text

# Load the model only once and keep preprocess
model, preprocess = load_model()  # ✅ Keeps preprocess for reuse


def generate_image_embedding(image_path):
    """
    Generates a CLIP embedding for an image.

    Args:
        image_path (str): Path to the image file.

    Returns:
        np.ndarray: Normalized image embedding.
    """
    image_tensor = preprocess_image(image_path, preprocess)  # ✅ Pass preprocess function
    if image_tensor is None:
        return None

    with torch.no_grad():
        image_features = model.encode_image(image_tensor)
    
    # Normalize the embedding
    image_features /= image_features.norm(dim=-1, keepdim=True)
    
    return image_features.cpu().numpy().astype(np.float32)

def generate_text_embedding(captions):
    """
    Generates a CLIP embedding for a list of text captions.

    Args:
        captions (list): List of captions.

    Returns:
        np.ndarray: Normalized text embedding.
    """
    text_tokens = tokenize_text(captions)
    if text_tokens is None:
        return None

    with torch.no_grad():
        text_features = model.encode_text(text_tokens)

    # Normalize the embeddings
    text_features /= text_features.norm(dim=-1, keepdim=True)

    # Compute averaged text embedding
    avg_text_embedding = text_features.mean(dim=0, keepdim=True)

    return avg_text_embedding.cpu().numpy().astype(np.float32)

def generate_joint_embedding(image_path, captions):
    """
    Generates a joint embedding by averaging image and text embeddings.

    Args:
        image_path (str): Path to the image file.
        captions (list): List of captions.

    Returns:
        np.ndarray: Normalized joint embedding.
    """
    image_embedding = generate_image_embedding(image_path)
    text_embedding = generate_text_embedding(captions)

    if image_embedding is None or text_embedding is None:
        print(f"⚠️ Skipping {image_path} due to missing embeddings.")
        return None

    # Compute joint embedding using averaging
    joint_embedding = (image_embedding + text_embedding) / 2

    # Normalize joint embedding
    joint_embedding /= np.linalg.norm(joint_embedding)

    return joint_embedding
