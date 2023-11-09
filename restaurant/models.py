from django.db import models


class Restaurant(models.Model):
    name = models.CharField(max_length=255, unique=True)
    address = models.TextField()

    def __str__(self):
        return self.name
