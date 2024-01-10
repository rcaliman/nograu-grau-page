from django import forms
from .models import ModelBikefit
from django.core.exceptions import ValidationError
class FormBikefit(forms.ModelForm):

    class Meta:
        model = ModelBikefit

        fields = [
            'cavalo',
            'esterno',
            'braco',
            'email',
        ]

    cavalo = forms.CharField(
        help_text= '''
            Uma das medidas mais importantes para determinar o tamanho do quadro.
            Fique totalmente encostado na parede e use um livro ou algo do tipo entre as pernas,
            o mais alto que puder, para medir a distância do chão ate o topo do objeto usado. 
        ''',
        widget=forms.NumberInput(attrs={'class': 'bikefit-input'}),
        error_messages={'required': 'A medida do cavalo é essencial para o cálculo'},
    )
    esterno = forms.CharField(
        help_text = '''
            Esta medida servirá para, junto com o tamanho do braço, determinar o
            comprimento total do quadro + mesa. Mede-se do chão ate a parte inferior da marca em V
            que temos acima do peito, onde fica o osso chamado esterno.
        ''',
        widget=forms.NumberInput(attrs={'class': 'bikefit-input'}),
        error_messages={'required': 'A medida do esterno é essencial para o cálculo'},
    )
    braco = forms.CharField(
        help_text = '''
            Estique o braço com o polegar para cima para medir conforme a foto ao lado.
        ''',
        widget=forms.NumberInput(attrs={'class': 'bikefit-input'}),
        error_messages={'required': 'A medida do braço é essencial para o cálculo'},
    )
    email = forms.EmailField(
        help_text = '''
            Por favor, digite seu email. Você pode usá-lo para recuperar seu cálculo através
            do ítem "cálculos anteriores" do menu.
        ''',
        widget=forms.EmailInput(attrs={'class': 'bikefit-email-input'}),
        error_messages={'required': 'Precisamos do email para salvar seu cálculo'},
    )
    def clean_cavalo(self):
        cavalo = self.cleaned_data.get('cavalo', '')
        if float(cavalo) < 3 or float(cavalo) > 200:
            raise ValidationError(
                'Confira este campo, ao que parece os dados estão incorretos. Lembre-se que vocẽ precisa informar suas medidas em centímetros',
                code='invalid',
            )
        return cavalo
    
    def clean_esterno(self):
        esterno = self.cleaned_data.get('esterno', '')
        if float(esterno) < 3 or float(esterno) > 250:
            raise ValidationError(
                'Confira este campo, ao que parece os dados estão incorretos. Lembre-se que vocẽ precisa informar suas medidas em centímetros',
                code='invalid',
                )
        return esterno
    
    def clean_braco(self):
        braco = self.cleaned_data.get('braco', '')
        if float(braco) < 3 or float(braco) > 200:
            raise ValidationError(
                'Confira este campo, ao que parece os dados estão incorretos. Lembre-se que vocẽ precisa informar suas medidas em centímetros',
                code='invalid'
            )
        return braco
    
class FormPreviousCalcs(forms.Form):
    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={'class': 'previous-email-input'},
        )
    )