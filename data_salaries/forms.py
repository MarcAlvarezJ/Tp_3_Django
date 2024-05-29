from django import forms

class upload_file(forms.Form):
    upload_file = forms.FileField(label='Base de datos')