from django.test import TestCase
from django.urls import reverse

class TestCalculoHoras(TestCase):
    def test_formulario(self):
        url = reverse('horas:horas')
        resposta = self.client.get(url, follow=True)
        self.assertIn('csrfmiddlewaretoken', resposta.content.decode('utf-8'))
        self.assertIn('<form method', resposta.content.decode('utf-8'))

    def test_formulario_resultado(self):
        self.dados = {
            'entrada': '9:00',
            'almoco': '12:00',
            'volta_almoco': '13:00',
            'saida': '16:00',
            'jornada': '6'
        }
        url = reverse('horas:horas')
        resposta = self.client.post(url, data=self.dados, follow=True)
        self.assertIn('Saída: 16:00:00', resposta.content.decode('utf-8'))

