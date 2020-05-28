from django.db import models

# Create your models here.

from django.db import models

class Writeup(models.Model):
    title = models.CharField(max_length=50, default="Title")
    image = models.URLField('Image')
    description = models.CharField(max_length=200)
    url = models.URLField('Github URL')
    year = models.IntegerField(default=2020)

    def __str__(self):
        return self.title

class Training_Domain(models.Model):
    title = models.CharField(max_length=50, default="Generic")
    slug = models.CharField(max_length=50, default=1)
    description = models.CharField(max_length=200, default="description")

    class Meta:
        verbose_name_plural = "Domains"

    def __str__(self):
        return self.title

class Training_Category(models.Model):
    title = models.CharField(max_length=50, default="Basic Skill")
    domain = models.ForeignKey(Training_Domain, default=1, verbose_name="Domain", on_delete=models.SET_DEFAULT)
    description = models.CharField(max_length=200, default="description")
    slug = models.CharField(max_length=50, default=1)

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.title

class Training(models.Model):
    title = models.CharField(max_length=50, default="Title")
    content = models.TextField()
    category = models.ForeignKey(Training_Category, default=1, verbose_name="Category", on_delete=models.SET_DEFAULT)
    slug = models.SlugField(max_length=50, default=1)

    def __str__(self):
        return self.title
