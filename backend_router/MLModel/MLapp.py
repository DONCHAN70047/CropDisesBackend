import numpy as np
import pickle
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
import os


ModelPath1 = os.getenv('ModelPath1')
ModelPath2 = os.getenv('ModelPath2')
model = load_model(ModelPath1)

with open(ModelPath2, "rb") as f:
    class_indices = pickle.load(f)


index_to_class = {v: k for k, v in class_indices.items()}


def predict_disease(img):
    """
    Accepts a PIL.Image.Image object.
    Preprocesses and predicts fire/no fire.
    Returns dictionary with predicted class + confidence.
    """
    img = img.resize((128, 128))  
    img_array = image.img_to_array(img)
    img_array = img_array / 255.0
    img_array = np.expand_dims(img_array, axis=0)

 
    predictions = model.predict(img_array)
    predicted_index = np.argmax(predictions[0])
    confidence = float(np.max(predictions[0]))
    predicted_class = index_to_class[predicted_index]

    return {"class": predicted_class, "confidence": confidence}
