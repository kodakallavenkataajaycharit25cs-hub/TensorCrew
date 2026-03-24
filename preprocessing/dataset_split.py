import os
import shutil
from pathlib import Path
from sklearn.model_selection import train_test_split
from tqdm import tqdm

CLEANED_DIR = Path("Data/cleaned")
TRAIN_DIR = Path("Data/train")
VAL_DIR = Path("Data/val")
TEST_DIR = Path("Data/test")

all_paths = []
all_labels = []
extensions = [".jpg", ".jpeg", ".png"]
print("--Gathering image paths and labels--")

for img_path in CLEANED_DIR.rglob("*"):
  if img_path.suffix.lower() in extensions:
    all_paths.append(img_path)
    all_labels.append(img_path.parent.name)
print(f"Found {len(all_paths)} healthy images across {len(set(all_labels))} classes")

train_paths, temp_paths, train_labels, temp_labels = train_test_split(
  all_paths, all_labels,
  test_size= 0.3,
  stratify= all_labels,
  random_state= 42
)

val_paths, test_paths, val_labels, test_labels = train_test_split(
  temp_paths, temp_labels,
  test_size= 0.5,
  stratify= temp_labels,
  random_state= 42
)

print(f"Training:   {len(train_paths)}")
print(f"Validation: {len(val_paths)}")
print(f"Testing:    {len(test_paths)}")

def move_files(paths, dest_base_dir, description):
  print(f"\n Moving files to {description}...")
  
  for path in tqdm(paths, desc= f"Copying to {description}"):
    class_name = path.parent.name
    dest_path = dest_base_dir / class_name / path.name
    dest_path.parent.mkdir(parents=True, exist_ok=True)
    
    shutil.copy2(path, dest_path)

move_files(train_paths, TRAIN_DIR, "Training Set")
move_files(val_paths, VAL_DIR, "Validation Set")
move_files(test_paths, TEST_DIR, "Test Set")
print("\n" + "="*50)
print("SUCCESS! Your dataset is now split 70/15/15.")
print(f"Train: {TRAIN_DIR}")
print(f"Val:   {VAL_DIR}")
print(f"Test:  {TEST_DIR}")