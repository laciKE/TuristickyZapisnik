from django.contrib import admin
from trips.models import Trip, Photo, Comment

class PhotoAdmin(admin.ModelAdmin):
	list_display = ['__unicode__', 'owner', 'trip', 'title', 'thumbnail']
	list_filter = ['trip']
	search_fields = ['title']

	def owner(self, photo):
		return photo.trip.owner

	def thumbnail(self, photo):
		return '<a href="' + photo.image.url + '"><img src="' + photo.thumb.url+'" alt="' + photo.title + '" width="40px" /></a>'
	thumbnail.allow_tags = True

admin.site.register(Trip)
admin.site.register(Photo, PhotoAdmin)
admin.site.register(Comment)
