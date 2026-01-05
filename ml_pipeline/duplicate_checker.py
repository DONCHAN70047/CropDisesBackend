import hashlib

def calculate_hash(image_bytes):
    return hashlib.sha256(image_bytes).hexdigest()
