from django import forms
from django.contrib.auth.models import User
from groups.models import CustomGroup

# Form with user-accessible fields from custom group model
class CustomGroupForm(forms.ModelForm):
	class Meta:
		model = CustomGroup
		fields = ('name',)
