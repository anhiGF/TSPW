from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Usuario
from captcha.fields import ReCaptchaField
from captcha.widgets import ReCaptchaV2Checkbox

class RegistroForm(UserCreationForm):
    captcha = ReCaptchaField(widget=ReCaptchaV2Checkbox)
    email = forms.EmailField(required=True)
    first_name = forms.CharField(required=True, label="Nombre")
    last_name = forms.CharField(required=True, label="Primer Apellido")
    segundo_apellido = forms.CharField(required=False, label="Segundo Apellido")
    fecha_nac = forms.DateField(required=True, label="Fecha de Nacimiento", widget=forms.DateInput(attrs={'type': 'date'}))
    tipo_usuario = forms.ChoiceField(choices=Usuario.TIPO_USUARIO_CHOICES, required=True)
    num_control = forms.IntegerField(required=True, label="Número de Control")
    semestre = forms.IntegerField(required=False, min_value=1, max_value=12)

    class Meta:
        model = Usuario
        fields = ('num_control', 'first_name', 'last_name', 'segundo_apellido', 'email', 
                  'tipo_usuario', 'semestre', 'fecha_nac', 'password1', 'password2')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.username = str(self.cleaned_data['num_control'])
        if commit:
            user.save()
        return user
    
