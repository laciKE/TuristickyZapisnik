from django import forms
from trips.models import Trip, Comment

# Form with user-accessible fields from trip model
class TripForm(forms.ModelForm):
	class Meta:
		model = Trip
		fields = ('title', 'trip_begin', 'trip_end', 'description', 'gpx_log', 'public')

	# add special class to datetime fields due to datetimepicker jquery plugin
	def __init__(self, *args, **kwargs):
		super(TripForm, self).__init__(*args, **kwargs)
		self.fields['trip_begin'].widget.attrs['class'] = 'datetimepicker'
 		self.fields['trip_end'].widget.attrs['class'] = 'datetimepicker'

# Form with user-accessible fields from comment model
class CommentForm(forms.ModelForm):
	class Meta:
		model = Comment
		fields = ('message',)
