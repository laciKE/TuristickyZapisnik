from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User

class CustomGroup(models.Model):
	name = models.CharField(_('name'), max_length=80)
	owner = models.ForeignKey(User)
	users = models.ManyToManyField(User, verbose_name=_('users'),
        blank=True, help_text=_('The users belongs to this group.'),
        related_name="custom_groups", related_query_name="group")

	def validate_unique_name_owner(self):        
		qs = CustomGroup.objects.filter(name=self.name)
		if qs.filter(owner=self.owner).exists():
			raise ValidationError(_('Name must be unique per user'))

	def save(self):
		self.validate_unique_name_owner()
		super(CustomGroup, self).save()

	def __unicode__(self):
		return self.name + '__' + self.owner.username
