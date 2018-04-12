from django.db import models

class Temperature(models.Model):
    degres = models.FloatField(default=-10)
    date_ajout = models.DateTimeField(auto_now_add=True,
                                      verbose_name="Date")

    class Meta:
        ordering = ['date_ajout']
        abstract = True

class TemperatureLac(Temperature):
    super

class TemperatureActuelle(Temperature):
    super

# class Graphique(models.Model):
#     date_ajout = models.DateTimeField(auto_now_add=True,
#                                       verbose_name="Date")
#     graph = models.ImageField(upload_to="graph/")
#
#     def __str__(self):
#            return self.date_ajout
