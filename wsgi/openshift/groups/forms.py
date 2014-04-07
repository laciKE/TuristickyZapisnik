from django import forms
from django.contrib.auth.models import User
from groups.models import CustomGroup

class CustomGroupForm(forms.ModelForm):
	class Meta:
		model = CustomGroup
		fields = ('name',)
