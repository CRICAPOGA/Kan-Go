from django import forms
from .models import Temporizadores

class PomodoroForm(forms.ModelForm):
    class Meta:
        model = Temporizadores
        fields = ['titulo', 'horas', 'minutos', 'segundos', 'prioridad']
        widgets = {
            'titulo': forms.TextInput(attrs={'required': 'required'}),
            'horas': forms.NumberInput(attrs={'required': 'required'}),
            'minutos': forms.NumberInput(attrs={'required': 'required'}),
            'segundos': forms.NumberInput(attrs={'required': 'required'}),
            'prioridad': forms.NumberInput(attrs={'required': 'required'}),
        }

    def clean(self):
        datos_limpios = super().clean()
        horas = datos_limpios.get('horas', 0)
        minutos = datos_limpios.get('minutos', 0)
        segundos = datos_limpios.get('segundos', 0)

        if horas < 0 or minutos < 0 or segundos < 0:
            raise forms.ValidationError("Las horas, minutos y segundos deben ser no negativos.")

        return datos_limpios
