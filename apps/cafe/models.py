from django.db import models

class ProdutorModel(models.Model):
    nome = models.CharField(max_length=200)
    localidade = models.CharField(max_length=200)
    cidade = models.CharField(max_length=200)
    estado = models.CharField(max_length=100)
    telefone = models.CharField(max_length=50)
    email = models.CharField(max_length=200)

    def __str__(self):
        return self.nome


class CafeModel(models.Model):
    especie = models.CharField(max_length=200)
    variedade = models.CharField(max_length=200)
    altitude = models.CharField(max_length=100)
    secagem = models.CharField(max_length=100)
    preco = models.CharField(max_length=50)
    produtor = models.ForeignKey(ProdutorModel, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.produtor.nome} - {self.variedade}'
    
class TorraModel(models.Model):
    temperatura_inicial = models.CharField(max_length=10)
    temperatura_final = models.CharField(max_length=10)
    temperatura_piso = models.CharField(max_length=10)
    fluxo_ar = models.CharField(max_length=10)
    velocidade_tambor = models.CharField(max_length=10)
    peso = models.CharField(max_length=10)
    data_torra = models.DateField()
    dados_torra = models.JSONField()
    cafe = models.ForeignKey(CafeModel, on_delete=models.CASCADE)
    observacoes = models.TextField(blank=True, null=True)

    def __str__(self):
        return f'{self.data_torra} - {self.cafe}'