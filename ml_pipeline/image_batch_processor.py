
import os
import django
import numpy as np


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Backend.settings")
django.setup()

from backend_router.models import DiseaseDetection
from ml_pipeline.data_cleaning import clean_image
from ml_pipeline.fuzzy_logic import fuzzy_scale
from ml_pipeline.train_model import train_model

BATCH_SIZE = 3
MODEL_SAVE_PATH = "ml_pipeline/ml_model.h5"

def process_batch():

    images = DiseaseDetection.objects.all()[:BATCH_SIZE]
    if not images:
        print("No images to process.")
        return

    X = []
    y = []


    for record in images:
        img_array = clean_image(record.image.path)
        X.append(img_array)
        y.append(record.predicted_disease)  

    X = np.array(X)
    y = np.array(y)


    predictions = [{"class": label, "confidence": 1.0} for label in y] 
    scaled_predictions = fuzzy_scale(predictions)
    print("Scaled Predictions:", scaled_predictions)

    
    class_to_index = {cls: i for i, cls in enumerate(sorted(set(y)))}
    y_indices = np.array([class_to_index[label] for label in y])

    
    train_model(X, y_indices, save_path=MODEL_SAVE_PATH)

   
    for record in images:
        try:
            os.remove(record.image.path)
        except Exception as e:
            print(f"Error deleting {record.image.path}: {e}")
        record.delete()

    print(f"Processed {len(images)} images and updated model.")

if __name__ == "__main__":
    process_batch()
