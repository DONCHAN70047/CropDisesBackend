import numpy as np
from backend_router.models import DiseaseDetection
from ml_pipeline.image_fetcher import fetch_image
from ml_pipeline.data_cleaning import clean_image
from ml_pipeline.duplicate_checker import calculate_hash
from ml_pipeline.train_model import train_incremental


LABEL_MAP = {
    "Brown Spot": 0,
    "Sheath Blight": 1,
    "Narrow Brown Leaf Spot": 2
}

def process_new_images():
    records = DiseaseDetection.objects.filter(is_processed=False)

    X, y = [], []

    for record in records:
        img = fetch_image(record)
        if img is None:
            record.is_processed = True
            record.save()
            continue

        # 🔹 Duplicate check
        image_bytes = img.tobytes()
        img_hash = calculate_hash(image_bytes)

        if DiseaseDetection.objects.filter(image_hash=img_hash).exclude(id=record.id).exists():
            record.is_processed = True
            record.save()
            print("Duplicate skipped")
            continue

        record.image_hash = img_hash
        record.save()

        # 🔹 Clean image (must return numeric array)
        clean_img = clean_image(img)

        # 🔴 SAFETY CHECK
        if record.predicted_disease not in LABEL_MAP:
            print(f"Unknown label skipped: {record.predicted_disease}")
            record.is_processed = True
            record.save()
            continue

        X.append(clean_img.astype(np.float32))
        y.append(LABEL_MAP[record.predicted_disease])

        record.is_processed = True
        record.save()

    if len(X) > 0:
        X = np.array(X, dtype=np.float32)
        y = np.array(y, dtype=np.int32)

        print("Training on:", X.shape, y.shape)
        train_incremental(X, y)
        print("Model trained with new data")
