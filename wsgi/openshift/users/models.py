from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
import os, Image
from uuid import uuid4

AVATAR_SIZE = (128, 128)
#helper function generating random names for avatars
def path_and_rename(path):
	def wrapper(instance, filename):
		ext = filename.split('.')[-1]
		# set filename as random string
		filename = '{0}.{1}'.format(uuid4().hex, ext.lower())
		# return the whole path to the file
		return os.path.join(path, filename)
	return wrapper

def resize_avatar(avatar):
	img = Image.open(avatar)
	w, h = img.size
	if w < h:
		img = img.crop((0, 0, w, w))
	else:
		img = img.crop(((w-h)/2, 0, w-(w-h)/2, h)) 
	img = img.resize(AVATAR_SIZE, Image.ANTIALIAS)
	img.save(avatar.path)


class UserProfile(models.Model):
	#extends model User
	user = models.OneToOneField(User)
	
	#additional attributes
	about_me = models.TextField(blank=True)
	avatar = models.ImageField(upload_to=path_and_rename('avatars'), blank=True, default='avatars/default.png')

	# Override the __unicode__() method to return out something meaningful!
	def __unicode__(self):
		return self.user.username

	# Override save() due to resize and crop avatar
	def save(self):
		super(UserProfile, self).save()
		resize_avatar(self.avatar)




