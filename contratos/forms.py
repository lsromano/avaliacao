from django import forms
from .models import Contrato, Alerta


class ContratoForm(forms.ModelForm) :


    class Meta :
        model = Contrato
        # campos que serão exibidos
        fields = [ 'contract_title', 'involved_parties', 'validity_start_date',
                   'validity_end_date', 'specific_clauses', 'description' ]

    def clean(self) :
        cleaned_data = super().clean()

        # Recuperando os valores de cada campo
        contract_title = cleaned_data.get('contract_title')
        involved_parties = cleaned_data.get('involved_parties')
        validity_start_date = cleaned_data.get('validity_start_date')
        validity_end_date = cleaned_data.get('validity_end_date')
        specific_clauses = cleaned_data.get('specific_clauses')
        description = cleaned_data.get('description')

        # verificação de cada campo para ver se está preenchido ou não, adicionado um erro ao campo correspondente
        if not contract_title :
            self.add_error('contract_title', 'Contract title is required.')

        if not involved_parties :
            self.add_error('involved_parties', 'Involved parties are required.')

        if not validity_start_date :
            self.add_error('validity_start_date', 'Validity start date is required.')

        if not validity_end_date :
            self.add_error('validity_end_date', 'Validity end date is required.')

        if not specific_clauses :
            self.add_error('specific_clauses', 'Specific clauses are required.')

        if not description :
            self.add_error('description', 'Description is required.')


class AlertaForm(forms.ModelForm): # 'mensagem' inativo.
    class Meta:
        model = Alerta
        fields = ['contrato', 'data_alerta', 'mensagem']
