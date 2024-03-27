from django import forms

jornada_choices = [
    (6, 6),
    (8, 8),
]


class FormHoras(forms.Form):
    entrada = forms.TimeField(required=True, widget=forms.TextInput(attrs={'type': 'time'}))
    almoco = forms.TimeField(required=False, widget=forms.TimeInput(attrs={'type': 'time'}))
    volta_almoco = forms.TimeField(required=False, widget=forms.TimeInput(attrs={'type': 'time'}))
    jornada = forms.ChoiceField(choices=jornada_choices, required=True)
