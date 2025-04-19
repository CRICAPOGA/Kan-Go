from django import forms
from .models import Tarea

# Formulario a partir del modelo
class TareaForm(forms.ModelForm):
    class Meta:
        model = Tarea
        # Campos
        fields = ['titulo', 'descripcion', 'es_urgente', 'es_importante', 'fecha_vencimiento']
        # Personalizar campos
        widgets = {
            'fecha_vencimiento': forms.DateInput(attrs={'type': 'date'}),
        }