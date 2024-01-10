from django.test import TestCase
from .calculator import Calculator
from apps.bikefit.models import ModelBikefit, ModelBikefitLinks, ModelBikefitAbout
from django.urls import reverse

class TestBikefit(TestCase):
    def setUp(self, *args, **kwargs):
        self.dados_bikefit = {
            'csrfmiddlewaretoken': 'abc123',
            'cavalo': ['90'],
            'esterno': ['160'],
            'braco': ['61'],
            'email': ['teste@teste.com'],
        }

        self.resultados_bikefit = {
            'cavalo': 90.0,
            'esterno': 160.0,
            'braco': 61.0,
            'email': 'teste@teste.com',
            'tronco': 70.0,
            'quadro_speed': 60.3,
            'quadro_mtb': 19.8,
            'altura_selim': 79.5,
            'top_tube_efetivo': 69.5,
            'data': None,
        }

        self.dados_calculos_anteriores = {
            'email': 'rcaliman@gmail.com',
        }
        return super().setUp(*args, **kwargs)
    
    def test_calcs_returns_correct_results(self):
        calculos = Calculator(**self.dados_bikefit).result()
        self.assertEqual(self.resultados_bikefit, calculos)

    def test_home_page(self):
        home = self.client.get('/')
        self.assertEqual(home.status_code, 200)

    def test_bikefit_form_page(self):
        formulario = self.client.get(reverse('bikefit:bikefit_form'))
        self.assertEqual(formulario.status_code, 200)

    def test_bikefit_wrong_values_cavalo_lower(self):
        self.dados_bikefit['cavalo'] = ['2']
        url = reverse('bikefit:bikefit_result')
        resposta = self.client.post(url, data=self.dados_bikefit, follow=True)
        self.assertIn('errorlist', resposta.content.decode('utf-8'))

    def test_bikefit_wrong_values_cavalo_upper(self):
        self.dados_bikefit['cavalo'] = ['201']
        url = reverse('bikefit:bikefit_result')
        resposta = self.client.post(url, data=self.dados_bikefit, follow=True)
        self.assertIn('errorlist', resposta.content.decode('utf-8'))

    def test_bikefit_wrong_values_esterno_lower(self):
        self.dados_bikefit['esterno'] = ['2']
        url = reverse('bikefit:bikefit_result')
        resposta = self.client.post(url, data=self.dados_bikefit, follow=True)
        self.assertIn('errorlist', resposta.content.decode('utf-8'))

    def test_bikefit_wrong_values_esterno_upper(self):
        self.dados_bikefit['esterno'] = ['251']
        url = reverse('bikefit:bikefit_result')
        resposta = self.client.post(url, data=self.dados_bikefit, follow=True)
        self.assertIn('errorlist', resposta.content.decode('utf-8'))

    def test_bikefit_wrong_values_braco_lower(self):
        self.dados_bikefit['braco'] = ['2']
        url = reverse('bikefit:bikefit_result')
        resposta = self.client.post(url, data=self.dados_bikefit, follow=True)
        self.assertIn('errorlist', resposta.content.decode('utf-8'))

    def test_bikefit_wrong_values_braco_upper(self):
        self.dados_bikefit['braco'] = ['201']
        url = reverse('bikefit:bikefit_result')
        resposta = self.client.post(url, data=self.dados_bikefit, follow=True)
        self.assertIn('errorlist', resposta.content.decode('utf-8'))

    def test_bikefit_result_page(self):
        url = reverse('bikefit:bikefit_result')
        resposta = self.client.post(url, data=self.dados_bikefit, follow=True)
        self.assertEqual(resposta.status_code, 200)

    def test_view_result(self):
        url = reverse('bikefit:bikefit_result')
        resposta = self.client.post(url, data=self.dados_bikefit, follow=True)
        self.assertIn('result', resposta.context)

    def test_view_previous_calcs(self):
        url = reverse('bikefit:previous_calcs')
        resposta = self.client.get(url)
        self.assertEqual(resposta.status_code, 200)

    def test_view_results_in_previous_calcs(self):
        url_bikefit_result = reverse("bikefit:bikefit_result")
        self.client.post(url_bikefit_result, data=self.dados_bikefit, follow=True)
        url_previous_calcs = reverse('bikefit:previous_calcs')
        email = {'email':'teste@teste.com'}
        resposta = self.client.post(url_previous_calcs, data=email, follow=True)
        self.assertIn('60,3', resposta.content.decode('utf-8'))
        self.assertIn('19,8', resposta.content.decode('utf-8'))
        self.assertIn('79,5', resposta.content.decode('utf-8'))
        self.assertIn('69,5', resposta.content.decode('utf-8'))

    def test_view_bikefit_links(self):
        url = reverse('bikefit:bikefit_links')
        resposta = self.client.get(url)
        self.assertIn('<h3 class="title-bike-fit">LINKS</h3>', resposta.content.decode('utf-8'))

    def test_view_bikefit_about(self):
        url = reverse('bikefit:bikefit_about')
        resposta = self.client.get(url)
        self.assertIn('<h3 class="title-bike-fit">SOBRE</h3>', resposta.content.decode('utf-8'))

    def test_view_bikefit_result_without_post(self):
        url = reverse('bikefit:bikefit_result')
        resposta = self.client.get(url)
        self.assertEqual(resposta.context['exception'], 'Http404')

    def test_view_bikefit_previous_calc_without_result(self):
        email = {'email': 'teste@teste1.com'}
        url = reverse('bikefit:previous_calcs')
        resposta = self.client.post(url, data=email, follow=True)
        self.assertIn('message-error', resposta.content.decode('utf-8'))

    def test_model_bikefit_returns_email_as__str__(self):
        model_bikefit = ModelBikefit(1, 90, 160, 161, 'teste@teste.com')
        self.assertEqual(str(model_bikefit), 'teste@teste.com')

    def test_model_bikefit_links_returns__str__(self):
        model_bikefit_links = ModelBikefitLinks(descricao='descricao', link='http://link.url')
        string = str(model_bikefit_links)
        self.assertEqual(string, 'descricao - http://link.url')

    def test_model_bikefit_about_returns__str__(self):
        model_bikefit_about = ModelBikefitAbout(
            titulo='titulo', nome='nome do cara', email='teste@teste.com', text='texto do about'
        )
        string = str(model_bikefit_about)
        self.assertEqual(string, 'nome do cara')
    
    
     