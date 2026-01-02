from PIL import Image
import numpy as np

def clean_image(image_path, target_size=(224, 224)):
    """
    Open an image, resize, convert to RGB and normalize
    """
    img = Image.open(image_path).convert("RGB")
    img = img.resize(target_size)
    img_array = np.array(img) / 255.0 
    return img_array
