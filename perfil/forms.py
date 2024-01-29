from django import forms
from django.contrib.auth.models import User
from .models import Perfil


class PerfilForm(forms.ModelForm):
    class Meta:
        model = Perfil
        fields = '__all__'
        exclude = ('usuario',)


class UserForm(forms.ModelForm):
    password = forms.CharField(
        required=False,
        widget=forms.PasswordInput(),
        label='Senha'
    )

    password2 = forms.CharField(
        required=False,
        widget=forms.PasswordInput(),
        label='Confirmar Senha'
    )

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username',
                  'password', 'password2', 'email')

    def __init__(self, usuario=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.usuario = usuario

    def clean(self, *args, **kwargs):
        cleaned = self.cleaned_data

        password_data = cleaned.get('password')
        password2_data = cleaned.get('password2')

        print(cleaned)
        if password_data != password2_data:
            self.add_error(
                'password',
                forms.ValidationError('Senhas não batem.')
            )
            self.add_error(
                'password2',
                forms.ValidationError('Senhas não batem.')
            )

    def clean_username(self, *args, **kwargs):
        cleaned = self.cleaned_data
        usuario_data = cleaned.get('username')
        usuario_db = User.objects.filter(username=usuario_data).first()

        user_exists = False

        if self.usuario:
            user_exists = (usuario_data != self.usuario.username
                           and usuario_db is not None)
        else:
            user_exists = usuario_db is not None

        if user_exists:
            self.add_error(
                'username',
                forms.ValidationError('Usuário já existe.')
            )

        return usuario_data

    def clean_email(self, *args, **kwargs):
        cleaned = self.cleaned_data
        email_data = cleaned.get('email')
        email_db = User.objects.filter(email=email_data).first()

        email_exists = False

        if self.usuario:
            email_exists = (email_data != self.usuario.email
                            and email_db is not None)
        else:
            email_exists = email_db is not None

        if email_exists:
            self.add_error(
                'email',
                forms.ValidationError('E-mail já existe.')
            )
        return email_data

    def clean_password(self, *args, **kwargs):
        cleaned = self.cleaned_data
        password_data = cleaned.get('password')

        if len(password_data) < 6:
            self.add_error(
                'password',
                forms.ValidationError('Senha deve ter no mínimo 6 caracteres.')
            )
        return password_data
