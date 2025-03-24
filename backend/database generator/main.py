import os
from glob import glob
from src.captions_loader import load_captions
from src.faiss_index import create_faiss_index, load_faiss_index
from config import BASE_PATH


def validate_images_with_captions(image_paths, captions_dict):
    mismatches = []

    # Extract image filenames from paths
    image_filenames = {os.path.basename(path) for path in image_paths}

    # Extract filenames from captions.txt
    caption_filenames = set(captions_dict.keys())

    # Find mismatches
    for filename in image_filenames:
        if filename not in caption_filenames:
            mismatches.append(f"❌ {filename} exists in images but not in captions.txt")

    for filename in caption_filenames:
        if filename not in image_filenames:
            mismatches.append(f"❌ {filename} exists in captions.txt but not in images")

    # Display results
    if mismatches:
        print("\n🔍 Mismatched Files:")
        for mismatch in mismatches:
            print(mismatch)
        print(f"\n⚠️ Total mismatches: {len(mismatches)}")
    else:
        print("\n✅ All images match with captions.txt")


def main():
    # Load captions
    captions_dict = load_captions()

    # Retrieve image file paths
    image_paths = glob(os.path.join(BASE_PATH, "*.jpg")) + glob(os.path.join(BASE_PATH, "*.jpeg"))

    print(f"✅ Found {len(image_paths)} images.")

    # Validate images with captions.txt
    validate_images_with_captions(image_paths, captions_dict)

    # Create and save FAISS index
    create_faiss_index(image_paths, captions_dict)

    # Load FAISS index (for verification)
    index, paths = load_faiss_index()
    if index is not None:
        print(f"✅ Loaded FAISS index with {index.ntotal} entries.")


if __name__ == "__main__":
    main()
