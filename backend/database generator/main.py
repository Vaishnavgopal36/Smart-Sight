import os
from glob import glob
from src.captions_loader import load_captions
from src.faiss_index import create_faiss_index, load_faiss_index
from config import BASE_PATH



def main():
    # Load captions
    captions_dict = load_captions()

    # Retrieve image file paths
    image_paths = glob(os.path.join(BASE_PATH, "*.jpg")) + glob(os.path.join(BASE_PATH, "*.jpeg"))

    print(f"✅ Found {len(image_paths)} images.")

    # Create and save FAISS index
    create_faiss_index(image_paths, captions_dict)

    # Load FAISS index (for verification)
    index, paths = load_faiss_index()
    if index is not None:
        print(f"✅ Loaded FAISS index with {index.ntotal} entries.")

if __name__ == "__main__":
    main()
