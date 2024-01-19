from django.test import TestCase
from django.urls import reverse
from apps.pcd.models import ModelPCD
from datetime import datetime

class TestPCD(TestCase):
    def setUp(self, *args, **kwargs):
        self.data_pcd = {
            'codigo_banco': '341',
            'proxima_parcela': '22012024',
            'ultima_parcela': '23122025',
            'quantidade_parcelas': '84',
            'valor_parcela': '25600',
            'valor_emprestado': '484196',
        }

        return super().setUp(*args, **kwargs)

    def test_form_pcd(self):
        url = reverse('pcd:pcd_form')
        resposta = self.client.get(url)
        self.assertIn('<form method', resposta.content.decode('utf-8'))

    def test_result_ispb(self):
        url = reverse('pcd:pcd_result')
        data = {'codigo_banco': '341'}
        resposta = self.client.post(url, data=data, follow=True)
        self.assertIn('60701190 - ITAÚ UNIBANCO S.A.', resposta.content.decode('utf-8'))
    

    def test_result_ispb_validate_numericos(self):
        url = reverse('pcd:pcd_result')
        data = {'codigo_banco': '34.1'}
        resposta = self.client.post(url, data=data, follow=True)
        self.assertIn('errorlist', resposta.content.decode('utf-8'))

    def test_result_pcd(self):
        url = reverse('pcd:pcd_result')
        data = self.data_pcd
        resposta = self.client.post(url, data=data, follow=True)
        valores = ['341', '22/01/2024', '23/12/2025', '84', 'R$ 256,00', 'R$ 4841,96', '5,21 %', '24', 'R$ 3460,37']
        for i in valores:
            self.assertIn(i, resposta.content.decode('utf-8'))
    
    def test_pcd_calculos_do_dia(self):
        url = reverse('pcd:pcd_calculos_do_dia')
        ModelPCD.objects.create(**self.data_pcd)
        ModelPCD.objects.create(**self.data_pcd)
        resposta = self.client.get(url, follow=True)
        valores = ['341', '22/01/2024', '23/12/2025', '84', 'R$ 256,00', 'R$ 4841,96', '5,21 %', '24', 'R$ 3460,37']
        for i in valores:
            self.assertIn(i, resposta.content.decode('utf-8'))

    def test_validate_form_pcd_apenas_numeros(self):
        self.data_pcd = {
            'codigo_banco': '34.1',
            'proxima_parcela': '220120.24',
            'ultima_parcela': '231220.25',
            'quantidade_parcelas': '84.1',
            'valor_parcela': '256.00',
            'valor_emprestado': '4841.96',
        }
        url = reverse('pcd:pcd_result')
        data = self.data_pcd
        resposta = self.client.post(url, data=data, follow=True)
        count = 0
        for i in resposta.content.decode('utf8').split('"'):
            if 'errorlist' in i:
                count += 1
        self.assertEqual(count, 6)

    def test_validate_form_pcd_campos_de_data_precisam_ter_6_digitos(self):
        self.data_pcd = {
            'codigo_banco': '341',
            'proxima_parcela': '220120241',
            'ultima_parcela': '2312225',
            'quantidade_parcelas': '841',
            'valor_parcela': '25600',
            'valor_emprestado': '484196',
        }
        url = reverse('pcd:pcd_result')
        data = self.data_pcd
        resposta = self.client.post(url, data=data, follow=True)
        count = 0
        for i in resposta.content.decode('utf8').split('"'):
            if 'errorlist' in i:
                count += 1
        self.assertEqual(count, 2)