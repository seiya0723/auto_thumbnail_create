from django import forms
from .models import Photo,Document


class PhotoForm(forms.ModelForm):

    class Meta:
        model   = Photo
        fields  = [ "file","user"]

class DocumentForm(forms.ModelForm):

    class Meta:
        model   = Document
        fields  = [ "file","mime" ]
