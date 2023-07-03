from django.shortcuts import render, redirect
from .forms import RegistrationForm
from django.contrib.auth import authenticate, login, update_session_auth_hash
from django.contrib import messages

def index(request) :
    if request.user.is_authenticated:  # Verifica se o usuário já está autenticado
        return redirect('contratos:contract_list')
    return render(request, 'autenticacao/index.html')


def forgot_view(request) :
    if request.user.is_authenticated:  # Verifica se o usuário já está autenticado
        return redirect('contratos:contract_list')
    return render(request, 'autenticacao/forgot.html')


def register_view(request) :
    if request.user.is_authenticated:  # Verifica se o usuário já está autenticado
        return redirect('contratos:contract_list')
    if request.method == 'POST' :
        form = RegistrationForm(request.POST)
        if form.is_valid() :
            try :
                email = form.cleaned_data.get('email')
                password = form.cleaned_data.get('password1')
                user = form.save(commit=False)
                user.username = email  # Define o email como username
                user.set_password(password)  # Define a senha
                user.save()
                messages.success(request, 'Registration successful. You can now log in.')
                login(request, user)  # Realizar login automático após o registro
                return redirect('autenticacao:index')
            except Exception as e :
                messages.error(request, f'Registration failed: {str(e)}')
        else :
            messages.error(request, 'Invalid form submission. Please check the form data.')
    else :
        form = RegistrationForm()
    return render(request, 'autenticacao/register.html', {'form' : form})


def login_submit(request) :
    if request.method == 'POST' :
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = authenticate(request, username=email, password=password)
        if user is not None :
            login(request, user)
            return redirect('contratos:contract_list')
        else :
            messages.error(request, 'Invalid email or password. Please try again.')

    return redirect('autenticacao:index')
