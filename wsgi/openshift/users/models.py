from django.db import models
from django.contrib.auth.models import User, Group

class UserProfile(models.Model):
	#extends model User
	user = models.OneToOneField(User)
	
	#additional attributes
	about_me = models.TextField(blank=True)
	avatar = models.ImageField(upload_to='avatars', blank=True)

	# Override the __unicode__() method to return out something meaningful!
	def __unicode__(self):
		return self.user.username

class MyGroup(models.Model):
	#extends model Group
	group = models.OneToOneField(Group)

	#additional attributes
	owner = models.ForeignKey(User)
