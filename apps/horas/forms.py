from django import forms

jornada_choices = [
    (6, 6),
    (7, 7),
    (8, 8),
]


class FormHoras(forms.Form):
    entrada = forms.TimeField(required=True, label='Entrada:', widget=forms.TextInput(attrs={'type': 'time'}))
    almoco = forms.TimeField(required=False, label='Almoço:', widget=forms.TimeInput(attrs={'type': 'time'}))
    volta_almoco = forms.TimeField(required=False, label='Volta do almoço:', widget=forms.TimeInput(attrs={'type': 'time'}))
    jornada = forms.ChoiceField(choices=jornada_choices, label='Jornada:', required=True)
