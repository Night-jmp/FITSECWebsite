from django.db import models
from django.contrib.auth.models import User 
from django.db.models.signals import post_save
from django.dispatch import receiver
from tinymce.models import HTMLField

# Create your models here.

class Category_Description(models.Model):
    title = models.CharField(max_length=50, default="Title")
    description = models.TextField()

    class Meta:
        ordering = ['title']
        verbose_name_plural = "Category Descriptions"
    
    def __str__(self):
        return self.title

class Writeup(models.Model):
    author = models.ForeignKey(User, null=True, on_delete=models.SET_NULL, default=1)
    # Change from github URL to textbox (preferrably an HTML editor box with tinymce)
    title = models.CharField(max_length=50, default="Title")
    #image = models.URLField('Image') # Don't really need this field
    description = models.CharField(max_length=200)
    slug = models.SlugField(max_length=50, default=1)
    content = HTMLField()
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
    author = models.ForeignKey(User, null=True, on_delete=models.SET_NULL, default=1)
    title = models.CharField(max_length=50, default="Title")
    content = HTMLField()
    category = models.ForeignKey(Training_Category, default=1, verbose_name="Category", on_delete=models.SET_DEFAULT)
    slug = models.SlugField(max_length=50, default=1)
    cat_description = models.ForeignKey(Category_Description, default=1, verbose_name="Cat", on_delete=models.SET_DEFAULT)
    challenge = models.FileField(upload_to="challenges", default="default")
    flag = models.CharField(max_length=50, default="Flag")
    user = models.ForeignKey(User, null=True, on_delete=models.SET_DEFAULT, default="none", related_name="user")
    
    class Meta:
        verbose_name_plural = "Modules"

    def __str__(self):
        return self.title

class TrainingCompletion(models.Model):
    module = models.ForeignKey(Training, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    completed = models.BooleanField()

    def __str__(self):
        return self.user.username


class Internship(models.Model):
    title = models.CharField(max_length=50, default="Internship Title")
    company = models.CharField(max_length=50, default="Company Name")
    state = models.CharField(max_length=50, default="State")
    city = models.CharField(max_length=50, default="City")
    website = models.URLField(max_length=50, default="URL")
    description = models.TextField()

    class Meta:
        verbose_name_plural = "Internships"

    def __str__(self):
        return self.title

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100, blank=True)
    last_name = models.CharField(max_length=100, blank=True)
    email = models.EmailField(max_length=150)
    signup_confirmation = models.BooleanField(default=False)
    fitcoins = models.IntegerField(default=0)

    def __str__(self):
        return self.user.username

@receiver(post_save, sender=User)
def update_profile_signal(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()

class StoreItem(models.Model):
    name = models.CharField(max_length=50, default="Item Name")
    price = models.IntegerField(default=999999)
    description = models.TextField()
    quantity = models.IntegerField(default=0)

    def __str__(self):
            return self.name

class Orders(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    item = models.ForeignKey(StoreItem, verbose_name="Order", on_delete=models.CASCADE)

    def __str__(self):
        return self.item.name


    class Meta:
        verbose_name_plural = "Orders"
