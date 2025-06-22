import os, hashlib, shutil

def hash_file(filepath):
    h = hashlib.sha256()
    with open(filepath, "rb") as f:
        while chunk := f.read(8192):
            h.update(chunk)
    return h.hexdigest()[:8]

def process_assets(src_dir, out_dir):
    os.makedirs(out_dir, exist_ok=True)
    for root, dirs, files in os.walk(src_dir):
        for file in files:
            if file.startswith('.'): continue
            src_path = os.path.join(root, file)
            h = hash_file(src_path)
            ext = os.path.splitext(file)[1]
            dest_name = f"{os.path.splitext(file)[0]}_{h}{ext}"
            dest_path = os.path.join(out_dir, dest_name)
            shutil.copy2(src_path, dest_path)