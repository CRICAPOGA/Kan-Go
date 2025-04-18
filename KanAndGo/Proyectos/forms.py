from django import forms
from .models import Proyecto

# Formulario a partir del modelo
class ProyectoForm(forms.ModelForm):
    class Meta:
        model = Proyecto 
        # Campos
        fields = ['nombre_proyecto', 'descripcion', 'fecha_finalizacion']
        # Personalizar campos
        widgets = {
            # área de texto con 4 filas
            'descripcion': forms.Textarea(attrs={'rows': 4}),
            # campo tipo fecha
            'fecha_finalizacion': forms.DateInput(attrs={'type': 'date'}),
        }