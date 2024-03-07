from django.test import TestCase
from apps.cafe.models import ProdutorModel, CafeModel, TorraModel
from django.contrib.auth.models import User
from datetime import datetime
from django.urls import reverse
import json

class TestCafe(TestCase):
    def setUp(self, *args, **kwargs):
        self.user = User.objects.create_user('temporario', 'temporario@teste.com', 'temporario')

        self.data_produtor = {
            'nome': 'joao produtor',
            'localidade': 'corrego bela aurora',
            'cidade': 'colatina',
            'estado': 'espirito santo',
            'telefone': '27999111609',
            'email': 'teste@teste.com',
        }
        self.produtor_pk = ProdutorModel.objects.create(**self.data_produtor).pk
        self.data_cafe = {
            'especie': 'arabica',
            'variedade': 'mundo novo',
            'altitude': '100',
            'secagem': 'natural',
            'preco': '100.0',
            'produtor': ProdutorModel.objects.get(pk=self.produtor_pk),
        }
        self.cafe_pk = CafeModel.objects.create(**self.data_cafe).pk
        self.data_torra = {
            'temperatura_inicial': '190',
            'temperatura_final': '210',
            'temperatura_piso': '90',
            'fluxo_ar': '80',
            'velocidade_tambor': '40',
            'peso': '100',
            'data_torra': datetime(2024, 10, 1),
            'dados_torra': {'1': '100', '2': '90', '3': '95', '4': '100', '5': '105', '6': '110', '7': '115', '8': '120'},
            'cafe': CafeModel.objects.get(pk=self.cafe_pk),
            'observacoes': 'teste de observações',
        }
        self.torra_pk = TorraModel.objects.create(**self.data_torra).pk
        return super().setUp(*args, **kwargs)
    
    def autenticar(self):
        url = reverse('cafe:cafe_login')
        user = {'username':'temporario', 'password':'temporario'}
        autenticacao = self.client.post(url, data=user, follow=True)
        return autenticacao
    
    def test_logout(self):
        self.autenticar()
        url = reverse('cafe:cafe_login') + '?logout=True'
        resposta = self.client.get(url, follow=True)
        self.assertIn('<form method=', resposta.content.decode('utf-8'))
    
    def test_tela_login(self):
        url = reverse('cafe:produtores')
        resposta = self.client.get(url, follow=True)
        self.assertIn("<button type=\'submit\'>Logar</button>", resposta.content.decode('utf-8'))

    def test_produtores(self):
        self.autenticar()
        url = reverse('cafe:produtores')
        resposta = self.client.get(url, follow=True)
        self.assertIn('joao produtor', resposta.content.decode('utf-8'))

    def test_produtor_form(self):
        self.autenticar()
        url = reverse('cafe:produtor_form')
        resposta = self.client.get(url, follow=True)
        self.assertIn('<form', resposta.content.decode('utf-8'))

    def test_produtor_inserir(self):
        self.autenticar()
        url = reverse('cafe:produtores')
        self.data_produtor['nome'] = 'jose produtor'
        resposta = self.client.post(url, data=self.data_produtor, follow=True)
        self.assertIn('joao produtor', resposta.content.decode('utf-8'))

    def test_produtor_apagar(self):
        self.autenticar()
        url = reverse('cafe:produtor_apagar', kwargs={'produtor_id': self.produtor_pk})
        resposta = self.client.get(url, follow=True)
        self.assertNotIn('joao produtor', resposta.content.decode('utf-8'))

    def test_produtor_editar(self):
        self.autenticar()
        url = reverse('cafe:produtor_editar', kwargs={'produtor_id': self.produtor_pk})
        resposta = self.client.get(url, follow=True)
        self.assertIn('joao produtor', resposta.content.decode('utf-8'))

    def test_produtor_editar_salvar(self):
        self.autenticar()
        url = reverse('cafe:produtores')
        self.data_produtor['produtor_id'] = self.produtor_pk
        self.data_produtor['nome'] = 'jose produtor'
        resposta = self.client.post(url, data=self.data_produtor, follow=True)
        self.assertIn('jose produtor', resposta.content.decode('utf-8'))


    def test_produtor(self):
        self.autenticar()
        url = reverse('cafe:produtor', kwargs={'produtor_id': self.produtor_pk})
        resposta = self.client.get(url, follow=True)
        self.assertIn('joao produtor', resposta.content.decode('utf-8'))

    def test_cafes(self):
        self.autenticar()
        url = reverse('cafe:cafes')
        resposta = self.client.get(url, follow=True)
        self.assertIn('arabica', resposta.content.decode('utf-8'))

    def test_cafe_form(self):
        self.autenticar()
        url = reverse('cafe:cafe_form')
        resposta = self.client.get(url, follow=True)
        self.assertIn('<form', resposta.content.decode('utf-8'))
        
    def test_cafe_editar(self):
        self.autenticar()
        url = reverse('cafe:cafe_editar', kwargs={'cafe_id': self.cafe_pk})
        resposta = self.client.get(url, follow=True)
        self.assertIn('<form', resposta.content.decode('utf-8'))
        self.assertIn('arabica', resposta.content.decode('utf-8'))

    def test_cafe_inserir(self):
        self.autenticar()
        url = reverse('cafe:cafes')
        self.data_cafe['especie'] = 'conilon'
        self.data_cafe['produtor'] = ProdutorModel.objects.first().pk
        resposta = self.client.post(url, data=self.data_cafe, follow=True)
        self.assertIn('arabica', resposta.content.decode('utf-8'))
        self.assertIn('conilon', resposta.content.decode('utf-8'))

    def test_cafe_editar_salvar(self):
        self.autenticar()
        url = reverse('cafe:cafes')
        self.data_cafe['cafe_id'] = self.cafe_pk
        self.data_cafe['especie'] = 'conilon'
        self.data_cafe['produtor'] = self.produtor_pk
        resposta = self.client.post(url, data=self.data_cafe, follow=True)
        self.assertIn('conilon', resposta.content.decode('utf-8'))


    def test_cafe_apagar(self):
        self.autenticar()
        url = reverse('cafe:cafe_apagar', kwargs={'cafe_id': self.cafe_pk})
        resposta = self.client.get(url, follow=True)
        self.assertNotIn('arabica', resposta.content.decode('utf-8'))

    def test_cafe(self):
        self.autenticar()
        url = reverse('cafe:cafe', kwargs={'cafe_id': self.cafe_pk})
        resposta = self.client.get(url, follow=True)
        self.assertIn('arabica', resposta.content.decode('utf-8'))

    def test_torras(self):
        self.autenticar()
        url = reverse('cafe:torras')
        resposta = self.client.get(url, follow=True)
        self.assertIn('01/10/2024', resposta.content.decode('utf-8'))

    def test_torras_adicionar(self):
        self.autenticar()
        url = reverse('cafe:torras')
        TorraModel.objects.get(id=self.torra_pk).delete()
        self.data_torra['data_torra'] = '2024-01-01'
        self.data_torra['cafe'] = self.cafe_pk
        resposta = self.client.post(url, data=self.data_torra, follow=True)
        self.assertIn('joao produtor - mundo novo', resposta.content.decode('utf-8'))

    def test_torra_apagar(self):
        self.autenticar()
        url = reverse('cafe:torra_apagar', kwargs={'torra_id': self.torra_pk})
        resposta = self.client.get(url, follow=True)
        self.assertNotIn('190', resposta.content.decode('utf-8'))
        self.assertNotIn('210', resposta.content.decode('utf-8'))


    def test_torras_editar(self):
        self.autenticar()
        url = reverse('cafe:torras')
        self.data_torra['data_torra'] = '2024-01-01'
        self.data_torra['cafe'] = self.cafe_pk
        self.data_torra['torra_id'] = self.torra_pk
        self.data_torra['temperatura_inicial'] = '666'
        self.data_torra['temperatura_final'] = '777'
        resposta = self.client.post(url, data=self.data_torra, follow=True)
        self.assertIn('666', resposta.content.decode('utf-8'))
        self.assertIn('777', resposta.content.decode('utf-8'))

        
    def test_torra_form(self):
        self.autenticar()
        url = reverse('cafe:torra_form')
        resposta = self.client.get(url, follow=True)
        self.assertIn('<form', resposta.content.decode('utf-8'))

    def test_torra_editar(self):
        self.autenticar()
        url = reverse('cafe:torra_editar', kwargs={'torra_id': self.torra_pk})
        resposta = self.client.get(url, follow=True)
        self.assertIn('<form', resposta.content.decode('utf-8'))
        self.assertIn('teste de observações', resposta.content.decode('utf-8'))

    def test_torra_nova_com_base(self):
        self.autenticar()
        url = reverse('cafe:torra_form')
        dados_torra = {'torra_id': [self.torra_pk]}
        resposta = self.client.post(url, data=dados_torra, follow=True)
        self.assertIn('DADOS DA TORRA BASE', resposta.content.decode('utf-8'))

    def test_torra_comparar(self):
        self.autenticar()
        url = reverse('cafe:torra_form')
        torra2_pk = TorraModel.objects.create(**self.data_torra).pk
        dados_torra = {'torra_id': [self.torra_pk, torra2_pk]}
        resposta = self.client.post(url, data=dados_torra, follow=True)
        self.assertIn('<img src="data:image/png;base64', resposta.content.decode('utf-8'))

    def test_torra(self):
        self.autenticar()
        url = reverse('cafe:torra', kwargs={'torra_id': self.torra_pk})
        resposta = self.client.get(url, follow=True)
        self.assertIn('01/10/2024', resposta.content.decode('utf-8'))
