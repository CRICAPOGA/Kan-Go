from django import forms
from .models import Etiqueta, DetalleEtiqueta

# Formulario para el modelo Etiqueta
class EtiquetaForm(forms.ModelForm):
    class Meta:
        model = Etiqueta
        fields = ['etiqueta', 'color']  # Excluir 'usuario_id'
        widgets = {
            'color': forms.TextInput(attrs={'type': 'color'}),  # Selector de color
        }

# Formulario para el modelo DetalleEtiqueta
class DetalleEtiquetaForm(forms.ModelForm):
    class Meta:
        model = DetalleEtiqueta
        fields = ['etiqueta_id', 'tarea_id']
        