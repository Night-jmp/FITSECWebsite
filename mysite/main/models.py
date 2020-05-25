from django.db import models

# Create your models here.

from django.db import models

class Writeup(models.Model):
    title = models.CharField(max_length=50, default="title")
    image = models.URLField('Image')
    description = models.CharField(max_length=200)
    url = models.URLField('Github URL')
    year = models.IntegerField(default=2020)

    def __str__(self):
        return self.title
