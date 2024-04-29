from django.shortcuts import render
from .form import UploadFileForm
from .load_model import extraxt_digit_from_image, load_model
import base64
#from django.http import HttpResponse

# Create your views here.
def index(request):

    if request.method == 'POST':
        formulario = UploadFileForm(request.POST, request.FILES)
        if formulario.is_valid():
            image_bytes = request.FILES['Image'].file.read()
            digit = extraxt_digit_from_image(image_bytes)
            # Codificar la imagen para ser utilizada en el HTML
            encoded_image = base64.b64encode(image_bytes).decode('utf-8')
            return render(request, 'index.html', {
                'formulario': formulario,
                'digit': digit,
                'image_src': 'data:image/jpeg;base64,' + encoded_image
            })
    else:
        formulario = UploadFileForm()
        return render(request, 'index.html', {'formulario': formulario})