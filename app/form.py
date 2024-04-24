from django import forms

class UploadFileForm(forms.Form):
    Image = forms.ImageField( required=True,)