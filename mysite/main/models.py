from django.db import models

# Create your models here.

class Category_Description(models.Model):
    title = models.CharField(max_length=50, default="Title")
    description = models.TextField()

    class Meta:
        ordering = ['title', 'description']
    
    def __str__(self):
        return self.title

class Writeup(models.Model):
    # Add author field
    # Change from github URL to textbox (preferrably an HTML editor box with tinymce)
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
    cat_description = models.ForeignKey(Category_Description, default=1, verbose_name="Cat", on_delete=models.SET_DEFAULT)

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.title

class Training(models.Model):
    title = models.CharField(max_length=50, default="Title")
    content = models.TextField()
    category = models.ForeignKey(Training_Category, default=1, verbose_name="Category", on_delete=models.SET_DEFAULT)
    slug = models.SlugField(max_length=50, default=1)
    cat_description = models.ForeignKey(Category_Description, default=1, verbose_name="Cat", on_delete=models.SET_DEFAULT)

    def __str__(self):
        return self.title

