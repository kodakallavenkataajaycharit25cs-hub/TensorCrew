import os
import pandas as pd
import shutil
import subprocess

def setup_ham10000():
    data_dir = 'Data'
    ham_dir = os.path.join(data_dir, 'ham10000')
    os.makedirs(ham_dir, exist_ok=True)

    print("Downloading HAM10000 dataset via Kaggle...")
    try:
        subprocess.run([
            'kaggle', 'datasets', 'download', '-d', 'kmader/skin-cancer-mnist-ham10000', '-p', ham_dir, '--unzip'
        ], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error downloading dataset: {e}")
        return

    metadata_path = os.path.join(ham_dir, 'HAM10000_metadata.csv')
    if not os.path.exists(metadata_path):
        print(f"Metadata file not found at {metadata_path}")
        return

    df = pd.read_csv(metadata_path)
    
    # HAM10000 images are in two folders: ham10000_images_part_1 and ham10000_images_part_2
    part1 = os.path.join(ham_dir, 'ham10000_images_part_1')
    part2 = os.path.join(ham_dir, 'ham10000_images_part_2')
    
    all_images_dir = os.path.join(ham_dir, 'all_images')
    os.makedirs(all_images_dir, exist_ok=True)

    print("Merging image parts...")
    for part in [part1, part2]:
        if os.path.exists(part):
            for img in os.listdir(part):
                shutil.move(os.path.join(part, img), os.path.join(all_images_dir, img))
    
    # Organize into train/val/test folders for ImageFolder compatibility
    # Classes: akiec, bcc, bkl, df, mel, nv, vasc
    classes = df['dx'].unique()
    
    for split in ['train', 'val', 'test']:
        for cls in classes:
            os.makedirs(os.path.join(data_dir, split, cls), exist_ok=True)

    print("Organizing images into class folders with splits...")
    # Simple split: 80% train, 10% val, 10% test (grouped by image_id)
    from sklearn.model_selection import train_test_split
    
    train_df, test_val_df = train_test_split(df, test_size=0.2, random_state=42, stratify=df['dx'])
    val_df, test_df = train_test_split(test_val_df, test_size=0.5, random_state=42, stratify=test_val_df['dx'])

    splits = {'train': train_df, 'val': val_df, 'test': test_df}

    for split_name, split_df in splits.items():
        print(f"Processing {split_name} split...")
        for _, row in split_df.iterrows():
            img_id = row['image_id'] + '.jpg'
            src = os.path.join(all_images_dir, img_id)
            dst = os.path.join(data_dir, split_name, row['dx'], img_id)
            if os.path.exists(src):
                shutil.copy(src, dst)
            else:
                # Some images might have .JPG extension
                src_alt = os.path.join(all_images_dir, row['image_id'] + '.JPG')
                if os.path.exists(src_alt):
                    shutil.copy(src_alt, dst)

    print("Dataset setup complete!")

if __name__ == "__main__":
    setup_ham10000()
