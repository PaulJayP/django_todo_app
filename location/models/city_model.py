from django.db import models
# Create your models here.


class City(models.Model):
    city_id = models.CharField(max_length=100)
    name = models.CharField(max_length=100,)
    country = models.ForeignKey('Country', on_delete=models.CASCADE)
    state = models.CharField(max_length=100, null=True)
    coord = models.JSONField()

    weather = models.JSONField(null=True)

    temp_code = models.CharField(max_length=20, null=True)
    temperature = models.CharField(max_length=10, null=True)

    objects = models.Manager()

    def __str__(self):
        return self.name
