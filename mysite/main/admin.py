from django.contrib import admin
from tinymce.widgets import TinyMCE
from django.db import models

from .models import *

class TrainingAdmin(admin.ModelAdmin):

    #formfield_overrides = {
    #        models.TextField: {'widget': TinyMCE(attrs={'cols': 80, 'rows': 30})},
    #        }
    pass

class WriteupAdmin(admin.ModelAdmin):

    #formfield_overrides = {
    #        models.TextField: {'widget': TinyMCE(attrs={'cols': 80, 'rows': 30})},
    #        }
    pass


admin.site.register(Writeup, WriteupAdmin)
admin.site.register(Training_Domain)
admin.site.register(Training_Category)
admin.site.register(Training, TrainingAdmin)
admin.site.register(Category_Description)
admin.site.register(Internship)
admin.site.register(TrainingCompletion)
admin.site.register(Profile)
admin.site.register(StoreItem)
