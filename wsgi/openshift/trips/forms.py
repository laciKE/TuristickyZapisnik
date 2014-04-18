from django import forms
from trips.models import Trip

class TripForm(forms.ModelForm):
	class Meta:
		model = Trip
		fields = ('title', 'trip_begin', 'trip_end', 'description', 'gpx_log')

	def __init__(self, *args, **kwargs):
		super(TripForm, self).__init__(*args, **kwargs)
		self.fields['trip_begin'].widget.attrs['class'] = 'datetimepicker'
 		self.fields['trip_end'].widget.attrs['class'] = 'datetimepicker'
