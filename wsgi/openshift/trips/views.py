from django.core.urlresolvers import reverse
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from django.shortcuts import get_object_or_404, render, render_to_response
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.http import HttpResponseRedirect, HttpResponse
from django.template.context import RequestContext
from trips.models import Trip
from trips.forms import TripForm

# Create your views here.


@login_required
def index(request):
	context = RequestContext(request)
	user = request.user
	trips = user.trip_set.all()
	trip_form = TripForm()
	return render_to_response('trips/index.html', {'trips': trips, 'form': trip_form}, context)

@login_required
def create(request):
	context = RequestContext(request)
	if request.method == 'POST':
		trip_form = TripForm(data=request.POST)
		print trip_form
		print request.POST
		if trip_form.is_valid():
			trip = trip_form.save(commit=False)
			user = request.user
			trip.owner = user
			if 'gpx_log' in request.FILES:
				trip.gpx_log = request.FILES['gpx_log']
			try:
				trip.save()
				print trip.trip_end, trip.trip_begin
	
				messages.success(request, _('Successfully created trip ') + trip.title)
				return HttpResponseRedirect(reverse('trips:index'))
			except ValidationError, e:
				messages.error(request, e.message)
		else:
			messages.error(request, trip_form.errors)
	else:
		trip_form = TripForm()

	return render_to_response('trips/create.html', {'form': trip_form}, context)

@login_required
def view(request, tripid):
	return HttpResponseRedirect(reverse('home'))


@login_required
def delete(request, tripid):
	context = RequestContext(request)
	user = request.user
	try:
		trip = Trip.objects.get(pk=tripid)
		if trip.owner == user:
			trip.delete()
			messages.info(request, _('Succesfully deleted trip ') + trip.name)
		else:
			messages.error(request, _('You have not permission to delete foreign trip.'))
	except Trip.DoesNotExist:
		messages.error(request, _('You can not delete non-existing trip.'))
	
	return HttpResponseRedirect(reverse('trips:index'))

@login_required
def edit(request, tripid):
	context = RequestContext(request)
	user = request.user
	try:
		trip = Trip.objects.get(pk=tripid)
		if trip.owner != user:
			messages.error(request, _('You have not permission to edit foreign trip.'))
			return HttpResponseRedirect(reverse('trips:index'))
	except Trip.DoesNotExist:
		messages.error(request, _('You are not allowed to edit non-existing group.'))
		return HttpResponseRedirect(reverse('trips:index'))
	
	return render_to_response('trips/edit.html', {'trip': trip, 'form': None}, context)
