from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class CustomUserCreationForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True, help_text='Obrigatório.')
    last_name = forms.CharField(max_length=30, required=True, help_text='Obrigatório.')
    email = forms.EmailField(max_length=254, required=True, help_text='Obrigatório. Informe um email válido.')

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'password1', 'password2')


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].label = 'Nome de usuário'
        self.fields['email'].label = 'Endereço de email'
        self.fields['first_name'].label = 'Nome'
        self.fields['last_name'].label = 'Sobrenome'
        self.fields['password1'].label = 'Senha'
        self.fields['password2'].label = 'Confirmação da senha'
        
        labels = {
            'username': 'Nome de usuário',
            'email': 'Endereço de email',
            'first_name': 'Nome',
            'last_name': 'Sobrenome',
            'password1': 'Senha',
            'password2': 'Confirmação da senha'
        }

        help_texts = {
            'username': 'Obrigatório. 150 caracteres ou menos. Letras, dígitos e @/./+/-/_ apenas.',
            'email': 'Obrigatório. Informe um email válido.',
            'first_name': 'Obrigatório.',
            'last_name': 'Obrigatório.',
            'password1': 'Sua senha não pode ser muito parecida com suas outras informações pessoais.',
            'password2': 'Digite a mesma senha novamente para verificação.'
        }
