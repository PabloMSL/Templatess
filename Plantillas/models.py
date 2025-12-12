from django.db import models
class monito(models.Model):
    nombre = models.CharField(max_length=100),
    tipo = models.CharField,
    existe = models.BooleanField,
    
    def __str__(self):
        return self.nombre
