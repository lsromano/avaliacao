from .models import Contrato, Alerta
from .forms import ContratoForm, AlertaForm
from django.utils import timezone
from django.http import HttpResponse # usar no download do pdf
from django.views.generic import DeleteView # usado para deletar contrato
from django.urls import reverse_lazy, reverse
from django.contrib.auth import logout as auth_logout  # auth_logout para nao confundir
from django.core.files.storage import FileSystemStorage # para guardar o pdf
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404 # retornar um erro 404 se o objeto não existir.
from django.contrib import messages # usar no lugar do alert
from datetime import date



# Função responsável por fazer o logout do usuário logado.
@login_required
def logout_view(request) :
    auth_logout(request)
    return redirect('index')


# Função responsável por exibir a lista de contratos.
@login_required
def contract_list(request) :
    today = date.today()
    alertas = Alerta.objects.filter(data_alerta=today)


    for alerta in alertas:
        messages.info(request, f"Alerta de Prazo: {alerta.contrato.contract_title}") # adiciona msg no objeto render

    # botao de pesquisa
    search_query = request.GET.get('search', '')   # variavel e definida obtendo o valor do parâmetro de consulta
    contratos = Contrato.objects.filter(user=request.user, contract_title__icontains=search_query)
    # retorna uma lista de contratos que corresponde ao filtro

    return render(request, 'contratos/contract_list.html', {'contratos' : contratos, 'search_query' : search_query})


# Função responsável por lidar com o formulário de criação de contratos.
@login_required
def contract_form(request) :
    if request.method == 'POST' :
        form = ContratoForm(request.POST, request.FILES)
        if form.is_valid() :
            messages.success(request, 'Alerta criado com sucesso!')

            contrato = form.save(commit=False)
            contrato.user = request.user  # Associar o contrato ao usuário logado

            # Processar o arquivo PDF enviado
            if 'attachment' in request.FILES :
                file = request.FILES[ 'attachment' ]
                fs = FileSystemStorage()
                filename = fs.save(file.name, file)
                contrato.attachment = filename

            contrato.ultima_atualizacao = timezone.now()  # Definir a data e hora da última atualização

            contrato.save()
            form.save_m2m() # estava bugando m2m = relacionamento muitos-para-muitos
            return redirect('contratos:contract_list')
    else :
        form = ContratoForm()

    return render(request, 'contratos/contract_form.html', {'form' : form})


#  exclusão de um contrato.
class ContractDeleteView(DeleteView) :
    model = Contrato
    success_url = reverse_lazy('contratos:contract_list') # redirecionar o usuário após a exclusão do objeto
    template_name = 'contratos/contract_confirm_delete.html'


# Função responsável por exibir informações de um contrato específico.
def contract_information(request, contract_id) :
    contrato = get_object_or_404(Contrato, pk=contract_id)

    selected_status = 'Active' if contrato.status == 'Active' else 'Inactive'
    historical_changes_url = reverse('contratos:historical_changes', args=[ contract_id ]) # link para visualizar as alterações

    return render(request, 'contratos/contract_information.html',
                  {'contrato' : contrato, 'historical_changes_url' : historical_changes_url})


# Função responsável por exibir as alterações históricas de um contrato.
def historical_changes(request, contract_id) :
    contrato = get_object_or_404(Contrato, pk=contract_id)
    return render(request, 'contratos/historical_changes.html', {'contrato' : contrato})


# Função responsável por atualizar um contrato existente
def contract_update(request, contrato_id) :
    contrato = get_object_or_404(Contrato, id=contrato_id)

    if request.method == 'POST' :
        form = ContratoForm(request.POST, instance=contrato)
        if form.is_valid() :
            contrato = form.save(commit=False)
            contrato.ultima_atualizacao = timezone.now()  # Atualizar a data e hora da última atualização
            contrato.status = request.POST.get('status')
            contrato.save()
            form.save_m2m()

            # Registrar as alterações no histórico
            alteracoes = form.changed_data
            contrato.registrar_alteracao(request.user, alteracoes)

            return redirect('contratos:contract_information', contract_id=contrato_id)

    else :
        form = ContratoForm(instance=contrato)

    return render(request, 'contratos/contract_information.html', {'contrato' : contrato, 'form' : form})


# Função responsável por baixar o anexo
def download_attachment(request, contrato_id) :
    contrato = get_object_or_404(Contrato, id=contrato_id)
    if contrato.attachment :
        file_path = contrato.attachment.path
        with open(file_path, 'rb') as file :
            response = HttpResponse(file.read(), content_type='application/pdf')
            response[ 'Content-Disposition' ] = f'attachment; filename="{contrato.attachment.name}"'
            return response
    return HttpResponse("File not found.")


@login_required
def criar_alerta(request) :
    if request.method == 'POST' :
        form = AlertaForm(request.POST)
        if form.is_valid() :
            alerta = form.save()
            return redirect('contratos:contract_information', contract_id=alerta.contrato.pk)
    else :
        form = AlertaForm()

    return render(request, 'contratos/criar_alerta.html', {'form' : form})

