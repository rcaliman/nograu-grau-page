from django.db import models

class ModelBikefit(models.Model):
    cavalo = models.FloatField()
    esterno = models.FloatField()
    braco = models.FloatField()
    email = models.EmailField()
    data = models.DateField(auto_now_add=True)

    class Meta:
        verbose_name = 'Cálculos de bikefit'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.email
        
class ModelBikefitLinks(models.Model):
    descricao = models.CharField(max_length=250)
    link = models.URLField()

    class Meta:
        verbose_name = 'Lista de Links'
        verbose_name_plural = verbose_name

    def __str__(self):
        return f'{self.descricao} - {self.link}'
    
class ModelBikefitAbout(models.Model):
    titulo = models.CharField(max_length=250)
    nome = models.CharField(max_length=250)
    email = models.EmailField()
    text = models.TextField()

    class Meta:
        verbose_name = 'Sobre'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.nome