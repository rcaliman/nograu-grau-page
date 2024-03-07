from django import forms
from apps.pcd.models import ModelPCD
from datetime import datetime
from django.core.exceptions import ValidationError

class FormModelPCD(forms.ModelForm):
    class Meta:
        model = ModelPCD

        fields = [
            'codigo_banco',
            'proxima_parcela',
            'ultima_parcela',
            'quantidade_parcelas',
            'valor_parcela',
            'valor_emprestado',
        ]

    codigo_banco = forms.CharField(
        widget=forms.NumberInput(attrs={'class': 'form-control'}),
        help_text='exemplo: 341',
        label='código do banco',
    )
    def clean_codigo_banco(self):
        codigo = self.cleaned_data['codigo_banco'].strip()
        if not codigo.isnumeric():
            raise ValidationError('digite apenas caracteres numéricos')
        if len(codigo) > 3:
            raise ValidationError('o código do banco deve ser o da compe, com no máximo 3 dígitos')
        return codigo
    
    proxima_parcela = forms.CharField(
        widget=forms.NumberInput(attrs={'class': 'form-control'}),
        help_text=f'exemplo: 0511{datetime.now().year}',
        label='próxima parcela',
    )
    def clean_proxima_parcela(self):
        proxima = self.cleaned_data['proxima_parcela'].strip()
        if not proxima.isnumeric():
            raise ValidationError('digite apenas caracteres numéricos')
        if len(proxima) != 8:
            raise ValidationError('digite 8 números conforme exemplo acima')
        return proxima
        

    ultima_parcela = forms.CharField(
        widget=forms.NumberInput(attrs={'class': 'form-control'}),
        help_text=f'exemplo: 0511{datetime.now().year + 4}',
        label='última parcela',
    )
    def clean_ultima_parcela(self):
        ultima = self.cleaned_data['ultima_parcela'].strip()
        if not ultima.isnumeric():
            raise ValidationError('digite apenas caracteres numéricos')
        if len(ultima) != 8:
            raise ValidationError('digite 8 números conforme exemplo acima')
        return ultima

    quantidade_parcelas = forms.CharField(
        widget=forms.NumberInput(attrs={'class': 'form-control'}),
        help_text='exemplo: 73',
        label='quantidade de parcelas',
    )
    def clean_quantidade_parcelas(self):
        quantidade = self.cleaned_data['quantidade_parcelas'].strip()
        if not quantidade.isnumeric():
            raise ValidationError('digite apenas caracteres numéricos')
        return quantidade

    valor_parcela = forms.CharField(
        widget=forms.NumberInput(attrs={'class': 'form-control'}),
        help_text='exemplo: 20307',
        label='valor da parcela',
    )
    def clean_valor_parcela(self):
        valor = self.cleaned_data['valor_parcela'].strip()
        if not valor.isnumeric():
            raise ValidationError('digite apenas caracteres numéricos')
        return valor
    
    valor_emprestado = forms.CharField(
        widget=forms.NumberInput(attrs={'class': 'form-control'}),
        help_text='exemplo: 749512 ',
        label='valor emprestado',
    )   
    def clean_valor_emprestado(self):
        valor = self.cleaned_data['valor_emprestado'].strip()
        if not valor.isnumeric():
            raise ValidationError('digite apenas caracteres numéricos')
        return valor



class FormISPB(forms.Form):

    codigo_banco = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        help_text='exemplo: 341',
        label='código do banco',
    )
    def clean_codigo_banco(self):
        codigo = self.cleaned_data['codigo_banco'].strip()
        if codigo.isnumeric():
            return codigo
        raise ValidationError('digite apenas caracteres numéricos')

