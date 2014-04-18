from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
from groups.models import CustomGroup
import os
from uuid import uuid4

#helper function generating random names for avatars
def path_and_rename(path):
	def wrapper(instance, filename):
		ext = filename.split('.')[-1]
		# set filename as random string
		filename = '{0}.{1}'.format(uuid4().hex, ext.lower())
		# return the whole path to the file
		return os.path.join(path, str(instance.owner.id), filename)
	return wrapper

class Trip(models.Model):

	#basic trip properties
	title = models.CharField(_('title'), max_length=80)
	owner = models.ForeignKey(User)
	trip_begin = models.DateTimeField(_('trip begin'))
	trip_end = models.DateTimeField(_('trip end'))
	description = models.TextField(_('description'), blank=True)
	gpx_log = models.FileField(upload_to=path_and_rename('gpx'), blank=True)
	
	#sharing options
	public = models.BooleanField(_('public trip'), default=False, help_text=_('If checked, everyone can view this trip regardless of sharing with users and/or groups'))
	share_users = models.ManyToManyField(User, verbose_name=_('share with users'),
        blank=True, help_text=_('The users sharing this trip.'),
        related_name="shared_trips", related_query_name="trips")
	share_groups = models.ManyToManyField(CustomGroup, verbose_name=_('share with groups'),
        blank=True, help_text=_('The groupss sharing this trip.'),
        related_name="shared_trips", related_query_name="trips")


	def validate_unique_title_owner(self):        
		qs = Trip.objects.filter(title=self.title)
		if qs.filter(owner=self.owner).exists():
			raise ValidationError(_('Trip title must be unique per user'))

	def save(self):
		self.validate_unique_title_owner()
		super(Trip, self).save()

	def __unicode__(self):
		return self.title + '__' + self.owner.username
