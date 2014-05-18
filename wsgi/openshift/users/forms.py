from django import forms
from django.contrib.auth.models import User
from users.models import UserProfile

# Form with useful fields for me from default user
class UserForm(forms.ModelForm):
	password = forms.CharField(widget=forms.PasswordInput())

	class Meta:
		model = User
		fields = ('username', 'email', 'first_name', 'last_name', 'password')

# Form with fields from default user which I want to be editable by signed-in user
class UserEditForm(forms.ModelForm):
	class Meta:
		model = User
		fields = ('email', 'first_name', 'last_name')

# Form with aditional fields for extended user and custom user profile
class UserProfileForm(forms.ModelForm):
	class Meta:
		model = UserProfile
		fields = ('about_me', 'avatar')
		widgets = {
			'avatar': forms.FileInput(),
		}
