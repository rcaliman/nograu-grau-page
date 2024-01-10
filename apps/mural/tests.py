from django.test import TestCase
from django.test.client import RequestFactory
from datetime import datetime
from django.urls import reverse
from apps.mural.models import ModelMural
from .pagination import make_pagination_range

class TestMural(TestCase):
    def setUp(self, *args, **kwargs):
        self.mural_data = {
            'nome': 'John Doe',
            'email': 'teste@teste.com',
            'mensagem': 'teste de mensagem',
            'data': datetime.now(),
        }
        self.factory = RequestFactory()
        return super().setUp(*args, **kwargs)
    
    def test_form_html_validate_in_nome(self):
        self.mural_data['nome'] = 'href'
        url = reverse('mural:mural')
        resultado = self.client.post(url, data=self.mural_data, follow=True)
        self.assertIn('errorlist', resultado.content.decode('utf-8'))
    
    def test_form_html_validate_in_mensagem(self):
        self.mural_data['mensagem'] = 'teste href teste'
        url = reverse('mural:mural')
        resultado = self.client.post(url, data=self.mural_data, follow=True)
        self.assertIn('errorlist', resultado.content.decode('utf-8'))

    def test_model_mural_returning__str__(self):
        model = str(ModelMural(**self.mural_data))
        string = model
        self.assertEqual(string, 'John Doe - teste@teste.com')

    def test_view_mural_form_valid(self):
        del(self.mural_data['data'])
        url = reverse('mural:mural')
        resposta = self.client.post(url, data=self.mural_data, follow=True)
        self.assertIn('John Doe', resposta.content.decode('utf-8'))

    def test_view_mural_form_invalid(self):
        del(self.mural_data['data'])
        self.mural_data['nome'] = 'href'
        url = reverse('mural:mural')
        resposta = self.client.post(url, data=self.mural_data, follow=True)
        self.assertIn('errorlist', resposta.content.decode('utf-8'))

    def test_view_mural_form_without_post(self):
        del(self.mural_data['data'])
        url = reverse('mural:mural')
        resposta = self.client.get(url)
        self.assertIn('MURAL DE MENSAGENS', resposta.content.decode('utf-8'))

    def test_pagination(self):
        pagination = make_pagination_range(
            page_range=list(range(1,21)),
            qty_pages=4,
            current_page=20,
        )['pagination']
        self.assertEqual([17, 18, 19, 20], pagination)

