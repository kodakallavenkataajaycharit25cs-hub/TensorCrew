import os
import shutil
import random
from pathlib import Path

CLEANED_DIR = Path("Data/cleaned")
TRAIN_DIR = Path("Data/train")
VAL_DIR = Path("Data/val")
TEST_DIR = Path("Data/test")

def split_dataset():
    classes = [d.name for d in CLEANED_DIR.iterdir() if d.is_dir()]
    
    for d in [TRAIN_DIR, VAL_DIR, TEST_DIR]:
        if d.exists():
            shutil.rmtree(d)
        d.mkdir(parents=True)

    for cls in classes:
        cls_path = CLEANED_DIR / cls
        images = list(cls_path.glob("*.jpg")) + list(cls_path.glob("*.png")) + list(cls_path.glob("*.jpeg"))
        random.shuffle(images)

        train_split = int(0.7 * len(images))
        val_split = int(0.15 * len(images)) + train_split

        train_imgs = images[:train_split]
        val_imgs = images[train_split:val_split]
        test_imgs = images[val_split:]

        for imgs, target_dir in zip([train_imgs, val_imgs, test_imgs], [TRAIN_DIR, VAL_DIR, TEST_DIR]):
            dest = target_dir / cls
            dest.mkdir(parents=True, exist_ok=True)
            for img in imgs:
                shutil.copy(img, dest / img.name)

    print("Dataset split successful.")
    print(f"Train: {TRAIN_DIR}")
    print(f"Val:   {VAL_DIR}")
    print(f"Test:  {TEST_DIR}")

if __name__ == "__main__":
    split_dataset()
