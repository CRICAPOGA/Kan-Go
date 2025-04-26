from django import forms
from django.core.exceptions import ValidationError
from .models import Temporizadores

class PomodoroForm(forms.ModelForm):
    class Meta:
        model = Temporizadores
        fields = ['titulo', 'horas', 'minutos', 'segundos', 'prioridad']
        widgets = {
            'titulo': forms.TextInput(attrs={'required': 'required', 'class': 'form-control'}),
            'horas': forms.NumberInput(attrs={'required': 'required', 'class': 'form-control'}),
            'minutos': forms.NumberInput(attrs={'required': 'required', 'class': 'form-control'}),
            'segundos': forms.NumberInput(attrs={'required': 'required', 'class': 'form-control'}),
            'prioridad': forms.NumberInput(attrs={'class': 'form-control', 'min': 1, 'max': 10}),
        }

    def __init__(self, *args, **kwargs):
        self.usuario = kwargs.pop('usuario', None)  # Extraer el argumento 'usuario'
        super().__init__(*args, **kwargs)

    def save(self, commit=True):
        instancia = super().save(commit=False)
        if self.usuario:
            instancia.usuario_id = self.usuario  # Asignar el usuario al temporizador
        if instancia.prioridad is None:
            instancia.prioridad = 1  # Valor predeterminado
        if commit:
            instancia.save()
        return instancia
