# backend/server/app/models.py
import torch
import clip
import faiss
import numpy as np
from PIL import Image
from settings import FAISS_INDEX_PATH, PATHS_FILE_PATH  # Updated import

device = "cuda" if torch.cuda.is_available() else "cpu"
model, preprocess = clip.load("ViT-B/32", device=device)

def load_faiss_index():
    index = faiss.read_index(FAISS_INDEX_PATH)
    with open(PATHS_FILE_PATH, 'r') as f:
        image_paths = [line.strip() for line in f]
    print("✅ FAISS index loaded successfully.")
    return index, image_paths

index, image_paths = load_faiss_index()