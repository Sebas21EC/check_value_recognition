from keras.models import load_model
from PIL import Image
import numpy as np
import io


model = load_model('app/data/model_Mnist.h5')
print('Model loaded......................')


def extraxt_digit_from_image(image_bytes):
    
    
    # Convertir la imagen a escala de grises
    image = Image.open(io.BytesIO(image_bytes)).convert('L')
    # Cambiar el tamaño de la imagen
    image = image.resize((28, 28))
    # Convertir la imagen a un arreglo de numpy
    image = np.array(image)
    # Normalizar la imagen
    image = image / 255
    # Cambiar la forma de la imagen
    image = image.reshape(1, 28, 28, 1)
    # Realizar la predicción
    prediction = model.predict([image])
    # Obtener el dígito predicho
    digit = np.argmax(prediction)
    return digit