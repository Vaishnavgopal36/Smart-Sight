# backend/server/app/utils.py
import torch
import numpy as np
from PIL import Image
import clip
import faiss
import os
import logging
from models import model, preprocess, index, image_paths
from settings import CAPTIONS_FILE_PATH

# Set up logging for debugging and verification
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def load_captions():
    """
    Load captions from the captions file into a dictionary with lowercase keys.
    Returns:
        dict: A dictionary mapping filenames to captions.
    """
    captions_dict = {}
    try:
        with open(CAPTIONS_FILE_PATH, 'r', encoding="utf-8") as f:
            for line in f:
                parts = line.strip().split(",", 1)
                if len(parts) == 2:
                    key = parts[0].strip().lower()  # Normalize to lowercase
                    captions_dict[key] = parts[1].strip()
                    logger.info(f"Loaded caption for {key}")
        logger.info(f"Loaded {len(captions_dict)} captions from {CAPTIONS_FILE_PATH}")
    except FileNotFoundError:
        logger.error(f"Captions file not found at {CAPTIONS_FILE_PATH}")
    except Exception as e:
        logger.error(f"Failed to load captions: {str(e)}")
    return captions_dict

captions_dict = load_captions()

def get_image_embedding(image: Image.Image):
    """
    Generate an embedding for the given image using the CLIP model.
    Args:
        image (PIL.Image.Image): The input image.
    Returns:
        numpy.ndarray: Normalized image embedding.
    """
    processed_image = preprocess(image).unsqueeze(0).to("cuda" if torch.cuda.is_available() else "cpu")
    with torch.no_grad():
        embedding = model.encode_image(processed_image).cpu().numpy()
    return embedding / np.linalg.norm(embedding)

def get_text_embedding(text: str):
    """
    Generate an embedding for the given text using the CLIP model.
    Args:
        text (str): The input text.
    Returns:
        numpy.ndarray: Normalized text embedding.
    """
    text_tokenized = clip.tokenize([text]).to("cuda" if torch.cuda.is_available() else "cpu")
    with torch.no_grad():
        embedding = model.encode_text(text_tokenized).cpu().numpy()
    return embedding / np.linalg.norm(embedding)

def get_joint_embedding(image: Image.Image, text: str):
    """
    Generate a joint embedding by averaging the image and text embeddings.
    Args:
        image (PIL.Image.Image): The input image.
        text (str): The input text.
    Returns:
        numpy.ndarray: Normalized joint embedding.
    """
    image_embedding = get_image_embedding(image)
    text_embedding = get_text_embedding(text)
    joint_embedding = (image_embedding + text_embedding) / 2
    return joint_embedding / np.linalg.norm(joint_embedding)


def search_faiss(query_embedding, top_k=1):
    # Search the FAISS index for the top_k most similar images and retrieve their captions.
    # Args:
    #     query_embedding (numpy.ndarray): The embedding to search with.
    #     top_k (int): Number of top results to return (default is 1).
    # Returns:
    #     list: A list of tuples containing (image_path, caption, similarity_score).

    distances, indices = index.search(query_embedding, top_k)
    results = []
    
    for i, idx in enumerate(indices[0]):
        if idx == -1:
            continue
        
        img_path = image_paths[idx]
        caption = captions_dict.get(os.path.basename(img_path).lower(), "No caption found")

        distance = distances[0][i]
        #similarity_score = 1 / (1 + distance)  # Converts L2 distance to similarity

        logger.info(f"Image: {img_path}, Distance: {distance}, Similarity: {distance*100:.2f}%")

        results.append((img_path, caption, distance))

    return results
