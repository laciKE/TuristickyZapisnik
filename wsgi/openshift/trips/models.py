from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
import os, Image
from uuid import uuid4
from datetime import datetime
from groups.models import CustomGroup

#helper function generating random names for avatars
def path_and_rename(path):
	def wrapper(instance, filename):
		ext = filename.split('.')[-1]
		# set filename as random string
		filename = '{0}.{1}'.format(uuid4().hex, ext.lower())
		# return the whole path to the file
		# check type of instance and determine correct save path
		if (type(instance) is Trip):
			return os.path.join(path, str(instance.owner.id), filename)
		else: # type(instance) is Photo
			return os.path.join(path, str(instance.trip.owner.id), filename)
	return wrapper

class Trip(models.Model):

	#basic trip properties
	title = models.CharField(_('title'), max_length=80)
	owner = models.ForeignKey(User)
	trip_begin = models.DateTimeField(_('trip begin'))
	trip_end = models.DateTimeField(_('trip end'))
	description = models.TextField(_('description'), blank=True)
	gpx_log = models.FileField(upload_to=path_and_rename('gpx'), blank=True)
	
	created = models.DateTimeField(auto_now_add=True)
	modified = models.DateTimeField(auto_now=True)

	#sharing options
	public = models.BooleanField(_('public trip'), default=False, help_text=_('If checked, everyone can view this trip regardless of sharing with users and/or groups'))
	share_users = models.ManyToManyField(User, verbose_name=_('share with users'),
        blank=True, help_text=_('The users sharing this trip.'),
        related_name="shared_trips", related_query_name="trips")
	share_groups = models.ManyToManyField(CustomGroup, verbose_name=_('share with groups'),
        blank=True, help_text=_('The groupss sharing this trip.'),
        related_name="shared_trips", related_query_name="trips")

	def validate_trip_begin_end(self):        
		if self.trip_begin > self.trip_end:
			raise ValidationError(_('Trip must ends after it begins'))

	def validate_unique_title_owner(self):        
		qs = Trip.objects.filter(title=self.title)
		if self.id:
			qs = qs.exclude(id=self.id)
		if qs.filter(owner=self.owner).exists():
			raise ValidationError(_('Trip title must be unique per user'))

	def save(self):
		self.validate_trip_begin_end()
		self.validate_unique_title_owner()
		super(Trip, self).save()

	# Override the __unicode__() method to return out something meaningful
	def __unicode__(self):
		return self.title + '__' + self.owner.username

class Photo(models.Model):
	trip = models.ForeignKey(Trip)
	title = models.CharField(_('title'), max_length=80, blank=True)
	image = models.ImageField(upload_to=path_and_rename('photos'), blank=False)
	thumb = models.ImageField(upload_to=path_and_rename('photos_thumb'), blank=True)

	# Override the __unicode__() method to return out something meaningful
	def __unicode__(self):
		return self.trip.title + '__' + os.path.basename(self.image.url)

	# Override save() due to create thumbnail of the photo
	def save(self):
		self.thumb.save(self.image.path, self.image, save=False)
		super(Photo, self).save()
		create_thumbnail(self.thumb)

THUMB_SIZE = (160, 160)
# create thumbnail from full-size photo image
def create_thumbnail(thumb):
	img = Image.open(thumb.path)
	w, h = img.size
	if w < h:
		img = img.crop((0, 0, w, w))
	else:
		img = img.crop(((w-h)/2, 0, w-(w-h)/2, h)) 
	img = img.resize(THUMB_SIZE, Image.ANTIALIAS)
	img.save(thumb.path)
