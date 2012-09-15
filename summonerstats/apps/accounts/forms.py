from django.forms import ModelForm, PasswordInput
from django.contrib.auth.models import User

class RegistrationForm(ModelForm):
    class Meta:
        model = User
        fields = ('username', 'password', 'email')
        widgets = {'password': PasswordInput()}
