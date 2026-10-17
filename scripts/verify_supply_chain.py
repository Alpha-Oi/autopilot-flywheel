import hashlib
import shutil
import json
import os

BINARIES = ["dcg", "cass", "bv", "ntm"]

def get_hash(path):
    if not path: return None
    h = hashlib.sha256()
    with open(path, 'rb') as f:
        while chunk := f.read(8192):
            h.update(chunk)
    return h.hexdigest()

def verify():
    results = {}
    for b in BINARIES:
        path = shutil.which(b)
        if path:
            results[b] = get_hash(path)
        else:
            results[b] = "not_found"
    
    with open("config/binaries.json", "w") as f:
        json.dump(results, f, indent=2)
    print("Хэши сохранены в config/binaries.json.")

if __name__ == "__main__":
    verify()
