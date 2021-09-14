import cv2
import numpy as np
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import img_to_array



class OCR():
	def __init__(self):
		self.loaded_model = None
		self.load_models()
		
	def load_models(self):

		self.loaded_model = load_model("digits.h5")

		return


	def prediction(self,image):

		image = cv2.resize(image, (28, 28))
		image = image.astype("float") / 255.0
		image = img_to_array(image)
		image = np.expand_dims(image, axis=0)

		predicted_val = self.loaded_model.predict(image,verbose=0).argmax(axis=1)[0]

		return predicted_val
