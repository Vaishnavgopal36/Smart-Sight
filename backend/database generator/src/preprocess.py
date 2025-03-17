from PIL import Image
import torch
import clip
from config import DEVICE
from src.model_loader import load_model

# Load the model (to get the preprocessing function)
_, preprocess = load_model()

def preprocess_image(image_path):
    """
    Loads and preprocesses an image for CLIP.

    Args:
        image_path (str): Path to the image file.

    Returns:
        torch.Tensor: Preprocessed image tensor.
    """
    try:
        image = Image.open(image_path).convert("RGB")
        return preprocess(image).unsqueeze(0).to(DEVICE)
    except Exception as e:
        print(f"❌ Error preprocessing image {image_path}: {e}")
        return None

def tokenize_text(captions):
    """
    Tokenizes a list of text captions for CLIP.

    Args:
        captions (list): List of captions.

    Returns:
        torch.Tensor: Tokenized text tensor.
    """
    try:
        return clip.tokenize(captions).to(DEVICE)
    except Exception as e:
        print(f"❌ Error tokenizing text: {e}")
        return None
