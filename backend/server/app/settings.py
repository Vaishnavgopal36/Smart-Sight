# backend/server/app/settings.py
from dotenv import load_dotenv
import os


load_dotenv()  # Load environment variables from .env file


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # backend/server/app/ → backend/server/
STATIC_DIR = os.path.join(BASE_DIR, "static")
FAISS_INDEX_PATH = os.path.abspath(os.path.join(BASE_DIR, "..", "database", "flickr8k_faiss_index.faiss"))
PATHS_FILE_PATH = os.path.abspath(os.path.join(BASE_DIR, "..", "database", "flickr8k_faiss_index.paths"))
CAPTIONS_FILE_PATH = os.path.abspath(os.path.join(BASE_DIR, "..", "database", "captions.txt"))
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Base API URL (set dynamically or use default)
API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8000")

def ensure_static_folder():
    """Ensure the static folder exists before use."""
    if not os.path.exists(STATIC_DIR):
        os.makedirs(STATIC_DIR)
        print(f"✅ Created missing static folder at: {STATIC_DIR}")
