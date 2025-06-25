from django import forms
from .models import OfertaLaboral

class OfertaLaboralForm(forms.ModelForm):
    class Meta:
        model = OfertaLaboral
        fields = ['titulo', 'descripcion', 'modalidad']
        widgets = {
            'descripcion': forms.Textarea(attrs={'rows': 4}),
        }