import clip
import torch
from config import DEVICE

def load_model(model_name="ViT-B/32"):
    """
    Loads the specified CLIP model and preprocessing function.

    Args:
        model_name (str): Name of the CLIP model to load.

    Returns:
        model: The loaded CLIP model.
        preprocess: The preprocessing function for images.
    """
    print(f"🔄 Loading CLIP model: {model_name} on {DEVICE}...")
    model, preprocess = clip.load(model_name, device=DEVICE)
    print("✅ Model loaded successfully!")
    return model, preprocess
