from django import forms

class UploadFileForm(forms.Form):
    title = forms.CharField( max_length=50, required=True, help_text='Titulo')
    Image = forms.ImageField( required=True, help_text='Imagen')