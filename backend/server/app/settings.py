# backend/server/app/settings.py
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # backend/server/app/ → backend/server/
STATIC_DIR = os.path.join(BASE_DIR, "static")
FAISS_INDEX_PATH = os.path.abspath(os.path.join(BASE_DIR, "..", "database", "flickr8k_faiss_index.faiss"))
PATHS_FILE_PATH = os.path.abspath(os.path.join(BASE_DIR, "..", "database", "flickr8k_faiss_index.paths"))
CAPTIONS_FILE_PATH = os.path.abspath(os.path.join(BASE_DIR, "..", "database", "captions.txt"))
GEMINI_API_KEY = "************"  # Replace with your actual key