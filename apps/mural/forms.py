from .models import ModelMural
from django import forms
from django.core.exceptions import ValidationError
from decouple import config

class FormModelMural(forms.ModelForm):
    mural_filtered_terms = config('MURAL_FILTERED_TERMS', cast=lambda x: [s.strip() for s in x.split(',')])
    mural_filtered_message = 'Desculpe, não aceitamos endereço web e tag html aqui.'

    class Meta:
        model = ModelMural

        fields = [
            'nome',
            'email',
            'mensagem',
        ]

    nome = forms.CharField(
        widget=forms.TextInput(
            attrs={'placeholder': 'Digite aqui o seu nome'}
        ),
        error_messages=({'required':'Desculpe, é obrigatório preencher o nome.'})
    )
    email= forms.EmailField(
        widget=forms.EmailInput(
            attrs={'placeholder': 'Digite aqui o seu email'}
        ),
        error_messages={'required': 'Desculpe, é obrigatório preencher o email.'}
    )
    mensagem = forms.CharField(
        widget=forms.Textarea(
            attrs={'placeholder': 'Digite aqui a sua mensagem'}
        ),
        error_messages={'required': 'Preencha seu texto por favor.'}
    )
    def clean_nome(self):
        nome = self.cleaned_data.get('nome', '')
        for term in self.mural_filtered_terms:
            if term in nome:
                raise ValidationError(self.mural_filtered_message)
        return nome
    
    def clean_mensagem(self):
        mensagem = self.cleaned_data.get('mensagem', '')
        for term in self.mural_filtered_terms:
            if term in mensagem:
                raise ValidationError(self.mural_filtered_message)
        return mensagem