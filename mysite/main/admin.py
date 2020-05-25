from django.contrib import admin
from tinymce.widgets import TinyMCE
from django.db import models

from .models import Writeup

admin.site.register(Writeup)
