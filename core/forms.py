from django import forms
from .models import Solicitud

class SolicitudForm(forms.ModelForm):
    class Meta:
        model = Solicitud
        fields = ['material', 'cantidad', 'fecha_estimada']
        widgets = {
            'fecha_estimada': forms.DateInput(attrs={'type': 'date'})
        }
