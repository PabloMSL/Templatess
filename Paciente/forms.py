from django import forms
from django.contrib.auth.models import User
from .models import Paciente

class RegistroUsuarioForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(label="Confirmar contraseña", widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError("Las contraseñas no coinciden")
        return cd['password2']

class RegistroPacienteForm(forms.ModelForm):
    class Meta:
        model = Paciente
        fields = ['nombre', 'telefono', 'fecha_nacimiento', 'direccion', 'tipo_sangre', 'alergias']
