from django.contrib import admin
from tinymce.widgets import TinyMCE
from django.db import models

from .models import Writeup, Training_Domain, Training_Category, Training

class TrainingAdmin(admin.ModelAdmin):

    formfield_overrides = {
            models.TextField: {'widget': TinyMCE(attrs={'cols': 80, 'rows': 30})},
            }

admin.site.register(Writeup)
admin.site.register(Training_Domain)
admin.site.register(Training_Category)
admin.site.register(Training, TrainingAdmin)
