from django.db import models
from django.utils.timezone import now
from django.contrib.auth.models import User
# Create your models here.
from location.models import City, Country


class TodoItem(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField(blank=True)
    created_at = models.DateTimeField(default=now, editable=False)
    updated_at = models.DateTimeField(editable=True, auto_now=True)
    completed_at = models.DateTimeField(blank=True, null=True, editable=True)

    user = models.ForeignKey(User, on_delete=models.CASCADE, editable=False)

    country = models.ForeignKey(Country, on_delete=models.SET_NULL, null=True)
    city = models.ForeignKey(City, on_delete=models.SET_NULL, null=True)

    objects = models.Manager()

    def __str__(self):
        return 'TodoItem(title={0}, content={1}, created_at={2}, updated_at={3}, completed_at={4})'.format(
            self.title,
            self.content,
            self.created_at,
            self.updated_at,
            self.completed_at,
        )
