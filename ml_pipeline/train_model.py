import tensorflow as tf
from tensorflow.keras.models import load_model
from tensorflow.keras.layers import Dense
from tensorflow.keras.optimizers import Adam

MODEL_PATH = "ml_pipeline/model.keras"
NUM_CLASSES = 3  # Brown Spot, Sheath Blight, Narrow BLB

def load_or_create_model():
    try:
        model = load_model(MODEL_PATH)
        print("Loaded existing model")
    except:
        base = tf.keras.applications.MobileNetV2(
            input_shape=(224,224,3),
            include_top=False,
            pooling="avg",
            weights="imagenet"
        )

        base.trainable = False

        model = tf.keras.Sequential([
            base,
            Dense(NUM_CLASSES, activation="softmax")
        ])

        model.compile(
            optimizer=Adam(1e-4),
            loss="sparse_categorical_crossentropy",
            metrics=["accuracy"]
        )

    return model

def train_incremental(X, y):
    model = load_or_create_model()

    model.fit(X, y, epochs=3, batch_size=8)

    model.save(MODEL_PATH)
    print("Model saved")
