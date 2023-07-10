
from django.db import models

class History(models.Model):
    tipo_acionamento = models.CharField(max_length=50)
    tipo_saida = models.CharField(max_length=50)
    data_acionamento = models.DateTimeField(auto_now_add=True)
    tempo_de_coleta = models.FloatField()

    def __str__(self):
        return f'{self.data_acionamento} - {self.tipo_acionamento}'


class Movie(models.Model):
    position = models.IntegerField('Posição')
    movie = models.CharField('Filme',max_length=255)
    year = models.CharField('Ano', max_length=255)
    duration = models.CharField('Duração',max_length=255)
    rating = models.CharField('Classificação indicativa',max_length=255)
    rate = models.FloatField('Nota')
    history = models.ForeignKey(History, on_delete=models.CASCADE)

    def __str__(self):
        return self.movie
