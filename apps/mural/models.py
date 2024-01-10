from django.db import models

class ModelMural(models.Model):
    nome = models.CharField(max_length=250)
    email = models.CharField(max_length=250)
    mensagem = models.TextField()
    data = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Mensagens do mural'
        verbose_name_plural = verbose_name

    def __str__(self):
        data = self.data.strftime('%d/%m/%Y - %H:%M:%S')
        return f'{data} - {self.nome} - {self.email}'
