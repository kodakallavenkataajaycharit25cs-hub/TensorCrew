import os
from PIL import Image
from pathlib import Path

RAW_DIR = Path("Data/raw")
CLEANED_DIR = Path("Data/cleaned")

def clean_data():
    if not CLEANED_DIR.exists():
        CLEANED_DIR.mkdir(parents=True)

    image_paths = list(RAW_DIR.glob("**/*.jpg")) + list(RAW_DIR.glob("**/*.png")) + list(RAW_DIR.glob("**/*.jpeg"))
    
    total_cleaned = 0
    total_skipped = 0

    for img_path in image_paths:
        try:
            img = Image.open(img_path)
            img.verify()
            
            relative_path = img_path.relative_to(RAW_DIR)
            save_path = CLEANED_DIR / relative_path
            save_path.parent.mkdir(parents=True, exist_ok=True)
            
            img = Image.open(img_path).convert("RGB")
            img.save(save_path)
            total_cleaned += 1
        except Exception:
            total_skipped += 1

    print(f"Cleaned: {total_cleaned} | Skipped: {total_skipped}")
    print(f"Done! Clean dataset ready in: {CLEANED_DIR}")

if __name__ == "__main__":
    clean_data()
