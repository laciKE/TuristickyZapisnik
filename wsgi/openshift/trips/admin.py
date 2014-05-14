from django.contrib import admin
from trips.models import Trip, Photo, Comment
# Register your models here.

admin.site.register(Trip)
admin.site.register(Photo)
admin.site.register(Comment)
