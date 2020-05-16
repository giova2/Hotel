from .models import Reservas, Contacto, Habitacion
from django import forms
import re

class ReservasForm(forms.ModelForm):
    # habitacion  = forms.IntegerField(required=True)
    nombre      = forms.CharField(max_length=40, required=True)
    email       = forms.EmailField(required=True)
    checkin     = forms.DateField(required=True)
    checkout    = forms.DateField(required=True)
    comentarios = forms.CharField(max_length=150, required=False)
    class Meta:
        model = Reservas
        exclude = ("cliente","estado",)

    def clean(self):
        cleaned_data = super().clean()
        checkin = cleaned_data.get("checkin")
        checkout = cleaned_data.get("checkout")
        if checkin and checkout and checkin > checkout:
            raise forms.ValidationError("La fecha de checkin debe ser menor o igual a la de checkout")

class ContactoForm(forms.ModelForm):
    nombre  = forms.CharField(max_length=100, required=True)
    email   = forms.EmailField(max_length=254, required=True)
    asunto  = forms.CharField(max_length=100, required=True)
    mensaje = forms.CharField(max_length=500, required=True)
    class Meta:
        model = Contacto
        exclude = ("respondido",)

    def clean(self):
        cleaned_data = super().clean()
        email   = cleaned_data.get("email")
        emailRegex = r"(?:[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*|\"(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21\x23-\x5b\x5d-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])*\")@(?:(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?|\[(?:(?:(2(5[0-5]|[0-4][0-9])|1[0-9][0-9]|[1-9]?[0-9]))\.){3}(?:(2(5[0-5]|[0-4][0-9])|1[0-9][0-9]|[1-9]?[0-9])|[a-z0-9-]*[a-z0-9]:(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21-\x5a\x53-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])+)\])"
        if re.match(emailRegex, email) is None:
            raise forms.ValidationError("la dirección de e-mail no es válida")