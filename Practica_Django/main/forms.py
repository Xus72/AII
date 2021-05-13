from django import forms
from .models import Maridaje

class MaridajeForm(forms.Form):
    busqueda = forms.ModelChoiceField(queryset=Maridaje.objects.all(), label='maridaje')

class AnyoForm(forms.Form):
    busqueda = forms.IntegerField(label="Año", widget=forms.TextInput, required=True)