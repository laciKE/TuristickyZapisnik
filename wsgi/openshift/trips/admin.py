from django.contrib import admin
from trips.models import Trip, Photo, Comment

class PhotoAdmin(admin.ModelAdmin):
	list_display = ('__unicode__', 'trip', 'title', 'thumbnail')

	def thumbnail(self, photo):
		return '<a href="' + photo.image.url + '"><img src="' + photo.thumb.url+'" alt="' + photo.title + '" width="40px" /></a>'
	thumbnail.allow_tags = True

admin.site.register(Trip)
admin.site.register(Photo, PhotoAdmin)
admin.site.register(Comment)
