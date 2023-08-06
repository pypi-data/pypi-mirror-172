import os

import tensorflow as tf
# try:
#     import importlib.resources as pkg_resources
# except ImportError:
#     import importlib_resources as pkg_resources

IMG_WIDTH = 320
IMG_HEIGHT = 240
IMG_CHANNELS = 3

class Segmentation:
    def __init__(self):
        # can be done better with importlib.resources
        pkg_path = os.path.abspath(__file__)
        model_path = os.path.join(os.path.dirname(pkg_path), 'models', 'multiclass_segmentation_model')
        self.model = tf.keras.models.load_model(model_path)
        self.model.summary()

    def predict(self, image):
        return self.model.predict(image.reshape((1,IMG_HEIGHT, IMG_WIDTH, IMG_CHANNELS)))

    def predict_batch(self, images):
        return self.model.predict(images.reshape((1,IMG_HEIGHT, IMG_WIDTH, IMG_CHANNELS)))

    def get_model(self):
        return self.model

    def get_model_summary(self):
        return self.model.summary()