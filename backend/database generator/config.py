import torch
import os

# Database paths (relative to backend directory)
BASE_PATH = os.path.join("..", "database", "images")
CAPTIONS_FILE_PATH = os.path.join("..", "database", "captions.txt")
OUTPUT_INDEX_PATH = os.path.join("..", "database", "flickr8k_faiss_index.faiss")
OUTPUT_PATHS_FILE = os.path.join("..", "database", "flickr8k_faiss_index.paths")

# Device (CPU or GPU)
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
