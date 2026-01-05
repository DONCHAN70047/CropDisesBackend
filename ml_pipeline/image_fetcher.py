import requests
import cv2
import numpy as np

def fetch_image(record):
    if record.image:
        return cv2.imread(record.image.path)

    if record.image_link.startswith("http"):
        resp = requests.get(record.image_link)
        img_arr = np.frombuffer(resp.content, np.uint8)
        return cv2.imdecode(img_arr, cv2.IMREAD_COLOR)

    return None
