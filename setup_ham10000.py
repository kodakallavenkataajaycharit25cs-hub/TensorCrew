import os
import pandas as pd
import shutil
from pathlib import Path
from sklearn.model_selection import train_test_split

def setup_ham10000():

    base_path = Path("Data/ham10000")
    raw_path = base_path / "raw"
    processed_path = base_path / "processed"
    
    for p in [raw_path, processed_path]:
        p.mkdir(parents=True, exist_ok=True)

    print("Downloading HAM10000 from Kaggle...")
    os.system(f"kaggle datasets download -d kmader/skin-cancer-mnist-ham10000 -p {raw_path} --unzip")


    print("Consolidating images...")
    all_images_dir = base_path / "all_images"
    all_images_dir.mkdir(exist_ok=True)
    
    parts = ["HAM10000_images_part_1", "HAM10000_images_part_2"]
    for part in parts:
        part_dir = raw_path / part
        if part_dir.exists():
            for img in part_dir.glob("*.jpg"):
                shutil.move(str(img), str(all_images_dir / img.name))


    df = pd.read_csv(raw_path / "HAM10000_metadata.csv")
    

    lesion_type_dict = {
        'nv': 'Melanocytic_nevi',
        'mel': 'Melanoma',
        'bkl': 'Benign_keratosis_like_lesions',
        'bcc': 'Basal_cell_carcinoma',
        'akiec': 'Actinic_keratoses',
        'vasc': 'Vascular_lesions',
        'df': 'Dermatofibroma'
    }
    df['label'] = df['dx'].map(lesion_type_dict)


    train_df, test_df = train_test_split(df, test_size=0.2, random_state=42, stratify=df['dx'])
    val_df, test_df = train_test_split(test_df, test_size=0.5, random_state=42, stratify=test_df['dx'])


    def move_to_folder(subset_df, subset_name):
        dest_root = base_path / subset_name
        for _, row in subset_df.iterrows():
            label = row['label']
            img_id = row['image_id']
            
            src = all_images_dir / f"{img_id}.jpg"
            dest_dir = dest_root / label
            dest_dir.mkdir(parents=True, exist_ok=True)
            
            if src.exists():
                shutil.copy(str(src), str(dest_dir / f"{img_id}.jpg"))

    print("Splitting into Train/Val/Test folders...")
    move_to_folder(train_df, 'train')
    move_to_folder(val_df, 'val')
    move_to_folder(test_df, 'test')

    print(f"\nSuccess! HAM10000 dataset ready in {base_path}")
    print(f"Classes: {list(lesion_type_dict.values())}")

if __name__ == "__main__":
    setup_ham10000()
