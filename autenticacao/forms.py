from django import forms
from .models import CustomUser
from django.contrib.auth.forms import UserCreationForm

#estendendo UserCreationForm
class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True) # campo obrigatorio

    class Meta:
        model = CustomUser #  formulário será baseado no modelo CustomUser
        fields = ('email', 'password1', 'password2')

    def clean_email(self):                              # validar se o email já está em uso, Personalização da validação
        email = self.cleaned_data.get('email')
        if CustomUser.objects.filter(email=email).exists():
            raise forms.ValidationError('This email is already in use.')
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user
