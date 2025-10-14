from django import forms

class LoginForm(forms.Form):
    email = forms.EmailField(label='Correo electrónico')
    password = forms.CharField(widget=forms.PasswordInput, label='Contraseña')

class RegisterForm(forms.Form):
    nombre = forms.CharField(max_length=60)
    apellido = forms.CharField(max_length=60)
    email = forms.EmailField(label='Correo electrónico')
    password = forms.CharField(widget=forms.PasswordInput, label='Contraseña')
    confirm = forms.CharField(widget=forms.PasswordInput, label='Confirmar contraseña')

    def clean(self):
        data = super().clean()
        if data.get('password') != data.get('confirm'):
            raise forms.ValidationError('Las contraseñas no coinciden')
        return data
