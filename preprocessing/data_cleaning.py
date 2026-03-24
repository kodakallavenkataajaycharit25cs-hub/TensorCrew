import os
from pathlib import Path
from PIL import Image
from tqdm import tqdm
from collections import defaultdict

RAW_DIR = Path("Data/raw") #Source 
CLEANED_DIR = Path("Data/cleaned") #Destination 
cleaning_stats = defaultdict(lambda :{ "total":0, "cleaned":0, "skipped":0 } )

def clean_convert(src_path, dest_path, class_name):
  cleaning_stats[class_name]["total"] += 1
  try:
    with Image.open(src_path) as img:
      img.verify() #Verifies Corruption
    
    with Image.open(src_path) as img:
      img = img.convert("RGB")
      dest_path.parent.mkdir(parents= True, exist_ok= True)
      img.save(dest_path, "JPEG", quality= 95)
      
      cleaning_stats[class_name]["cleaned"] += 1
      return True
  except Exception:
    cleaning_stats[class_name]["skipped"] += 1
    return False

def run_cleaning():
  extensions = [".jpg", ".jpeg", ".png"]
  all_files = list(RAW_DIR.rglob("*"))
  image_paths = [p for p in all_files if p.suffix.lower() in extensions]
  
  print(f"Found {len(image_paths)} images. Starting clean up: ")
  for img_path in tqdm(image_paths, desc= "Scrubbing Data"):
    class_name = img_path.parent.name
    relative_path = img_path.relative_to(RAW_DIR)
    dest_path = CLEANED_DIR / relative_path
    clean_convert(img_path, dest_path, class_name)
  
  print("\n" + "="*50)
  print(f"{'CLASS NAME':<40} | {'CLEANED':<7} | {'SKIPPED'}")
  print("-" * 60)

  total_cleaned = 0
  total_skipped = 0

  for cls, s in sorted(cleaning_stats.items()):
    print(f"{cls[:40]:<40} | {s['cleaned']:<7} | {s['skipped']}")
    total_cleaned += s['cleaned']
    total_skipped += s['skipped']

  print("-" * 60)
  print(f"{'TOTAL':<40} | {total_cleaned:<7} | {total_skipped}")
  print("="*50)
  print(f"✅ Done! Clean dataset ready in: {CLEANED_DIR}")

if __name__ == "__main__":
  run_cleaning()