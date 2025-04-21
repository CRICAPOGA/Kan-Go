from django import forms
from .models import Usuario

# Formulario a partir del modelo
class UsuarioForm(forms.ModelForm):
    class Meta:
        model = Usuario
        # Campos
        fields = ['nombre', 'apellido', 'username', 'correo', 'rol_id']
        # Personalizar campos
        widgets = {
            'rol_id': forms.Select(attrs={'class': 'form-control'}),
        }