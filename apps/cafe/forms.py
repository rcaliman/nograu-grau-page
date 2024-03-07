from django import forms
from .models import ProdutorModel, CafeModel, TorraModel


class LoginForm(forms.Form):
    username = forms.CharField(
        max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    password = forms.CharField(
        max_length=100, widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )


class ProdutorForm(forms.ModelForm):
    class Meta:
        model = ProdutorModel
        fields = "__all__"
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control'}),
            'localidade': forms.TextInput(attrs={'class': 'form-control'}),
            'cidade': forms.TextInput(attrs={'class': 'form-control'}),
            'estado': forms.TextInput(attrs={'class': 'form-control'}),
            'telefone': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'nome': 'Nome do Produtor:',
            'localidade': 'Localidade:',
            'cidade': 'Cidade:',
            'estado': 'Estado:',
            'telefone': 'Telefone:',
            'email': 'E-mail:',
        }


class CafeForm(forms.ModelForm):
    class Meta:
        model = CafeModel
        fields = "__all__"
        widgets = {
            'especie': forms.TextInput(attrs={'class': 'form-control'}),
            'variedade': forms.TextInput(attrs={'class': 'form-control'}),
            'altitude': forms.NumberInput(attrs={'class': 'form-control'}),
            'secagem': forms.TextInput(attrs={'class': 'form-control'}),
            'preco': forms.NumberInput(attrs={'class': 'form-control'}),
            'produtor': forms.TextInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'especie': 'Espécie:',
            'variedade': 'Variedade:',
            'altitude': 'Altitude:',
            'secagem': 'Secagem:',
            'preco': 'Preço:',
            'produtor': 'Produtor:',
        }

class TorraForm(forms.ModelForm):
    class Meta:
        model = TorraModel
        fields = "__all__"
        widgets = {
            'temperatura_inicial': forms.NumberInput(attrs={'class': 'form-control'}),
            'temperatura_final': forms.NumberInput(attrs={'class': 'form-control'}),
            'temperatura_piso': forms.NumberInput(attrs={'class': 'form-control'}),
            'fluxo_ar': forms.NumberInput(attrs={'class': 'form-control'}),
            'velocidade_tambor': forms.NumberInput(attrs={'class': 'form-control'}),
            'peso': forms.NumberInput(attrs={'class': 'form-control'}),
            'data_torra': forms.DateInput(attrs={'class': 'form-control'}),
            'dados_torra': forms.HiddenInput(),
            'cafe': forms.Select(attrs={'class': 'form-control'}),
            'observacoes': forms.TextInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'temperatura_inicial': 'Tempratura inicial:',
            'temperatura_final': 'Temperatura final:',
            'temperatura_piso': 'Temperatura mais baixa:',
            'fluxo_ar': 'Fluxo de ar:',
            'velocidade_tambor': 'Velocidade do tambor:',
            'peso': 'Peso:',
            'data_torra': 'Data da torra:',
            'dados_torra': '',
            'cafe': 'Café:',
            'observacoes': 'Observações:',
        }