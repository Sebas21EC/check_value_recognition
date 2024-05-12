from django.shortcuts import render
from .form import UploadFileForm
from .load_model import extract_check, crop_interest_area, extract_digit_from_image,detect_and_crop_digit
import base64
import cv2
import numpy as np

def index(request):
    if request.method == 'POST':
        formulario = UploadFileForm(request.POST, request.FILES)
        if formulario.is_valid():
            image_bytes = request.FILES['Image'].read()
            nparr = np.frombuffer(image_bytes, np.uint8) 
            image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

            if image is None or image.size == 0:
                print("Error: The image failed to load or is empty.")
                return render(request, 'index.html', {'formulario': formulario, 'error': 'Failed to load image.'})

            image_check = extract_check(image)
            cropped_image = crop_interest_area(image_check)
            cropped_digit = detect_and_crop_digit(cropped_image)
            digits = extract_digit_from_image(cropped_digit)
            number_check = "".join(map(str, digits))

            image_check = cv2.cvtColor(image_check, cv2.COLOR_GRAY2BGR)
            _, encoded_image = cv2.imencode('.png', image_check)
            image_check = base64.b64encode(encoded_image).decode('utf-8')

            image_interest_area = cv2.cvtColor(cropped_image, cv2.COLOR_GRAY2BGR)
            _, encoded_image = cv2.imencode('.png', image_interest_area)
            image_interest_area = base64.b64encode(encoded_image).decode('utf-8')

            return render(request, 'index.html', {
    'formulario': formulario,
    'number_check': number_check,
    'image_check': 'data:image/png;base64,' + image_check,
    'image_interest_area': 'data:image/png;base64,' + image_interest_area,
})

    else:
        formulario = UploadFileForm()
        return render(request, 'index.html', {'formulario': formulario})
