from django.db import models

# Create your models here.
class Lang(models.Model):
    lang = models.CharField(max_length=255, default='')

# class Station(models.Model):
#     ids = models.IntegerField(default=0)
#     dist = models.IntegerField(default=0)
#     kf = models.IntegerField(default=0)

class City(models.Model):
    id = models.IntegerField(primary_key=True, default=0)
    lon = models.FloatField(default=0.0)
    lat = models.FloatField(default=0.0)
    country = models.CharField(max_length=5, default='')
    cl = models.CharField(max_length=5, default='')
    code = models.CharField(max_length=5, default='')
    parent = models.IntegerField(default=0)
    langs = models.ManyToManyField(Lang)
    name = models.CharField(max_length=255, default='')
    level = models.FloatField(default=0.0)
    population = models.IntegerField(default=0)
    # stations = models.ManyToManyField(Station)
    # zoom = models.IntegerField(default=0)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'cities'