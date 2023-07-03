from django.contrib.auth.models import AbstractUser
from django.contrib.auth import password_validation
from django.db import models

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)  # Adiciona o campo de email

    class Meta:
        db_table = 'autenticacao_customuser'

    def save(self, *args, **kwargs):
        # Executar as validações de senha antes de salvar o usuário
        password_validation.validate_password(self.password)
        super().save(*args, **kwargs)
