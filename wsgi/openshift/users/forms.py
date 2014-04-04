from django import forms
from django.contrib.auth.models import User
from users.models import UserProfile

class UserForm(forms.ModelForm):
	password = forms.CharField(widget=forms.PasswordInput())

	class Meta:
		model = User
		fields = ('username', 'email', 'first_name', 'last_name', 'password')

class UserEditForm(forms.ModelForm):
	class Meta:
		model = User
		fields = ('email', 'first_name', 'last_name')

class UserProfileForm(forms.ModelForm):
	class Meta:
		model = UserProfile
		fields = ('about_me', 'avatar')
		widgets = {
			'avatar': forms.FileInput(),
		}
