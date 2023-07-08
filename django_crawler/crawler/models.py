from django.db import models

# Create your models here.
from django.db import models

class History(models.Model):
    tipo_acionamento = models.CharField(max_length=50)
    data_acionamento = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.data_acionamento} - {self.tipo_acionamento}'


class Movie(models.Model):
    position = models.IntegerField('Posição',  primary_key=True)
    movie = models.CharField('Filme',max_length=255)
    year = models.DateField('Ano')
    duration = models.CharField('Duração',max_length=255)
    rating = models.CharField('Classificação indicativa',max_length=255)
    rate = models.FloatField('Nota')

    def __str__(self):
        return self.movie
