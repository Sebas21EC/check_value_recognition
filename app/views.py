from django.shortcuts import render
from .form import UploadFileForm
from .load_model import extraxt_digit_from_image
#from django.http import HttpResponse

# Create your views here.
#muestrame el hola mundo con https

def index(request):

    if request.method == 'POST':
        formulario = UploadFileForm(request.POST, request.FILES)
        if formulario.is_valid():
            image_bytes = request.FILES['Image'].file.read()
            digit = extraxt_digit_from_image(image_bytes)
            return render(request, 'index.html', {'formulario': formulario, 'digit': digit})
    else:

        formulario = UploadFileForm()
        return render(request, 'index.html', {'formulario': formulario})