from django.db import models


class Country(models.Model):
    name = models.CharField(max_length=50, unique=True)

    objects = models.Manager()

    def __str__(self):
        return self.name
