from django.contrib import admin

# Register your models here.
from .models import Photo,Document

admin.site.register(Photo)
admin.site.register(Document)
