import faiss
import numpy as np
import os
from tqdm import tqdm
from src.embeddings import generate_joint_embedding
from config import OUTPUT_INDEX_PATH, OUTPUT_PATHS_FILE

def create_faiss_index(image_paths, captions_dict):
    """
    Creates and saves a FAISS index for image-text embeddings.

    Args:
        image_paths (list): List of image file paths.
        captions_dict (dict): Dictionary mapping image filenames to captions.

    Returns:
        None
    """
    embeddings = []
    image_paths_list = []

    for image_path in tqdm(image_paths, total=len(image_paths)):
        img_name = os.path.basename(image_path)
        captions = captions_dict.get(img_name, ["No Caption Available"])

        # Generate joint embedding
        joint_embedding = generate_joint_embedding(image_path, captions)

        if joint_embedding is None:
            print(f"⚠️ Skipping {image_path} due to missing embeddings.")
            continue

        embeddings.append(joint_embedding)
        image_paths_list.append(image_path)

    if not embeddings:
        print("❌ No embeddings generated. Please check input data.")
        return

    embeddings = np.vstack(embeddings).astype(np.float32)

    # Create FAISS index
    index = faiss.IndexFlatIP(embeddings.shape[1])
    index.add(embeddings)

    # Save FAISS index
    faiss.write_index(index, OUTPUT_INDEX_PATH)

    # Save image paths
    with open(OUTPUT_PATHS_FILE, 'w') as f:
        for path in image_paths_list:
            f.write(path + '\n')

    print(f"✅ FAISS index saved at {OUTPUT_INDEX_PATH}")
    print(f"✅ Image paths saved at {OUTPUT_PATHS_FILE}")

def load_faiss_index():
    """
    Loads the FAISS index and associated image paths.

    Returns:
        index (faiss.Index): The FAISS index.
        image_paths (list): List of image paths.
    """
    if not os.path.exists(OUTPUT_INDEX_PATH) or not os.path.exists(OUTPUT_PATHS_FILE):
        print("❌ FAISS index or paths file not found.")
        return None, []

    # Load FAISS index
    index = faiss.read_index(OUTPUT_INDEX_PATH)

    # Load image paths
    with open(OUTPUT_PATHS_FILE, 'r') as f:
        image_paths = [line.strip() for line in f]

    print(f"✅ FAISS index loaded from {OUTPUT_INDEX_PATH}")
    return index, image_paths
