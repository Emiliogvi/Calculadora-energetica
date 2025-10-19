from django import forms
from .models import Electrodomestico

class LoginForm(forms.Form):
    email = forms.EmailField(label="Correo electrónico")
    password = forms.CharField(widget=forms.PasswordInput, label="Contraseña")

class RegisterForm(forms.Form):
    nombre = forms.CharField(max_length=30, label="Nombre")
    apellido = forms.CharField(max_length=30, label="Apellido")
    email = forms.EmailField(label="Correo electrónico")
    password = forms.CharField(widget=forms.PasswordInput, label="Contraseña")
    password2 = forms.CharField(widget=forms.PasswordInput, label="Confirmar contraseña")

    # Validar correo único
    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Ya existe una cuenta con este correo")
        return email

    # Validar que las contraseñas coincidan
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password2 = cleaned_data.get("password2")
        if password and password2 and password != password2:
            self.add_error("password2", "Las contraseñas no coinciden")
        return cleaned_data

        
class ElectrodomesticoForm(forms.ModelForm):
    class Meta:
        model = Electrodomestico
        fields = ['nombre', 'categoria', 'tipo', 'potencia_w', 'horas_uso_diario']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'categoria': forms.Select(attrs={'class': 'form-control'}),
            'tipo': forms.Select(attrs={'class': 'form-control'}),
            'potencia_w': forms.NumberInput(attrs={'class': 'form-control', 'min': 0}),
            'horas_uso_diario': forms.NumberInput(attrs={'class': 'form-control', 'min': 0, 'max': 24}),
        }