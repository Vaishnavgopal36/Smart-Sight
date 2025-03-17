from collections import defaultdict
import os
from config import CAPTIONS_FILE_PATH

def load_captions(captions_file=CAPTIONS_FILE_PATH):
    """
    Loads captions from a file and stores them in a dictionary.

    Args:
        captions_file (str): Path to the captions file.

    Returns:
        dict: A dictionary mapping image filenames to their captions.
    """
    captions_dict = defaultdict(list)

    if not os.path.exists(captions_file):
        print(f"❌ Captions file not found: {captions_file}")
        return captions_dict

    try:
        with open(captions_file, 'r', encoding="utf-8") as f:
            for line in f:
                parts = line.strip().split(',', 1)  # Expect "image_name,caption"
                if len(parts) == 2:
                    img_name, caption = parts
                    captions_dict[img_name].append(caption)

        print(f"✅ Loaded captions for {len(captions_dict)} images.")

    except Exception as e:
        print(f"❌ Error loading captions file: {e}")

    return captions_dict
