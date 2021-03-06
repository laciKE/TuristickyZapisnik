from django.core.urlresolvers import reverse
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from django.shortcuts import get_object_or_404, render, render_to_response
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.http import HttpResponseRedirect, HttpResponse
from django.template.context import RequestContext
from django.views.decorators.csrf import csrf_protect
from groups.models import CustomGroup
from trips.models import Trip, Comment, Photo
from trips.forms import TripForm, CommentForm


# view for display list of user's trips
@login_required
def index(request):
	context = RequestContext(request)
	user = request.user
	trips = user.trip_set.all().order_by('-id')
	return render_to_response('trips/index.html', {'trips': trips}, context)


# view for display list of all users public trips
def public(request):
	context = RequestContext(request)
	trips = Trip.objects.filter(public=True).order_by('-id')
	return render_to_response('trips/public.html', {'trips': trips}, context)


# view for display handle creation of new trip
@csrf_protect
@login_required
def create(request):
	context = RequestContext(request)
	if request.method == 'POST':
		trip_form = TripForm(data=request.POST)
		if trip_form.is_valid():
			trip = trip_form.save(commit=False)
			user = request.user
			trip.owner = user
			if 'gpx_log' in request.FILES:
				trip.gpx_log = request.FILES['gpx_log']
			try:
				trip.save()
				messages.success(request, _('Successfully created trip ') + trip.title)
				return HttpResponseRedirect(reverse('trips:index'))
			except ValidationError, e:
				messages.error(request, e.message)
		else:
			messages.error(request, trip_form.errors)
	else:
		trip_form = TripForm()

	return render_to_response('trips/create.html', {'form': trip_form}, context)


# view for display information about concrete trip
def view(request, tripid):
	context = RequestContext(request)
	user = request.user
	try:
		trip = Trip.objects.get(pk=tripid)
		if __shared_trip(trip, user):
			photos = trip.photo_set.all()
			comments = trip.comment_set.all().order_by('-id')
			comment_form = None
			if (user.is_authenticated()):
				comment_form = CommentForm()
			return render_to_response('trips/view.html', {'trip': trip, 'photos': photos, 'comments': comments, 'comment_form': comment_form}, context)
		else:
			messages.error(request, _('You are not allowed to view this trip.'))
	except Trip.DoesNotExist:
		messages.error(request, _('You can not view non-existing trip.'))
	
	return HttpResponseRedirect(reverse('home'))

# view for handle adding comments to the trip
@csrf_protect
@login_required
def add_comment(request, tripid):
	context = RequestContext(request)
	user = request.user
	try:
		trip = Trip.objects.get(pk=tripid)
		if __shared_trip(trip, user):
			if request.method == 'POST':
				comment_form = CommentForm(data=request.POST)
				if comment_form.is_valid():
					comment = comment_form.save(commit=False)
					comment.author = user
					comment.trip = trip
					try:
						comment.save()
						messages.success(request, _('Successfully added comment.'))
					except ValidationError, e:
						messages.error(request, e.message)
				else:
					messages.error(request, comment_form.errors)

			return HttpResponseRedirect(reverse('trips:view', args=(tripid,)))
		else:
			messages.error(request, _('You are not allowed to comment this trip.'))

	except Trip.DoesNotExist:
		messages.error(request, _('You can not comment non-existing trip.'))
	
	return HttpResponseRedirect(reverse('home'))


# view for handle adding photos to the trip
@csrf_protect
@login_required
def add_photos(request, tripid):
	context = RequestContext(request)
	user = request.user
	try:
		trip = Trip.objects.get(pk=tripid)
		if __shared_trip(trip, user):
			if (request.method == 'POST') and ('file' in request.FILES):
				photo = Photo(image=request.FILES['file'])
				photo.trip = trip
				try:
					photo.save()
					#messages.success(request, _('Successfully upload photo.'))
					return render_to_response('trips/photos_add.html', {'photo': photo}, context)					
				except ValidationError, e:
					messages.error(request, e.message)

			return HttpResponseRedirect(reverse('trips:edit_photos', args=(tripid,)))

		else:
			messages.error(request, _('You are not allowed to add photo to this trip.'))
			return HttpResponseRedirect(reverse('trips:view', args=(tripid,)))


	except Trip.DoesNotExist:
		messages.error(request, _('You can not add photo to non-existing trip.'))
	
	return HttpResponseRedirect(reverse('home'))


# view for display and handle editation photos from the trip
@csrf_protect
@login_required
def edit_photos(request, tripid):
	context = RequestContext(request)
	user = request.user
	try:
		trip = Trip.objects.get(pk=tripid)
		photos = trip.photo_set.all()
		if __shared_trip(trip, user):
			if request.method == 'POST':
				try:
					for photo in photos:
						id = str(photo.id)
						if request.POST.has_key(id):
							edited_photo = request.POST.get(id)
							if photo.title != edited_photo:
								photo.title = edited_photo
								photo.save()
						else:
							photo.delete()

					photos = trip.photo_set.all()
					messages.success(request, _('Successfully edited photos.'))
				except ValidationError, e:
					messages.error(request, e.message)
				except ValueError, e:
					messages.error(request, e.message)

			return render_to_response('trips/photos_edit.html', {'trip': trip, 'photos': photos}, context)

		else:
			messages.error(request, _('You are not allowed to edit photos of this trip.'))
			return HttpResponseRedirect(reverse('trips:view', args=(tripid,)))

	except Trip.DoesNotExist:
		messages.error(request, _('You can not edit photos of non-existing trip.'))
	
	return HttpResponseRedirect(reverse('home'))


# view for handle delete the trip
@login_required
def delete(request, tripid):
	context = RequestContext(request)
	user = request.user
	try:
		trip = Trip.objects.get(pk=tripid)
		if trip.owner == user:
			trip.delete()
			messages.info(request, _('Succesfully deleted trip ') + trip.title)
		else:
			messages.error(request, _('You have not permission to delete foreign trip.'))
	except Trip.DoesNotExist:
		messages.error(request, _('You can not delete non-existing trip.'))
	
	return HttpResponseRedirect(reverse('trips:index'))


# view for display and handle editation of the trip
@csrf_protect
@login_required
def edit(request, tripid):
	context = RequestContext(request)
	user = request.user
	try:
		trip = Trip.objects.get(pk=tripid)
		if trip.owner != user:
			messages.error(request, _('You have not permission to edit foreign trip.'))
			return HttpResponseRedirect(reverse('trips:index'))
		if request.method == 'POST':
			trip_form = TripForm(data=request.POST, instance=trip)
			if trip_form.is_valid():
				trip = trip_form.save(commit=False)
				if 'gpx_log' in request.FILES:
					trip.gpx_log = request.FILES['gpx_log']
				try:
					trip.save()
					messages.success(request, _('Successfully edited trip ') + trip.title)
					#trip_form = TripForm(instance=trip) #for refreshing gpx log
					return HttpResponseRedirect(reverse('trips:view', args=(tripid,)))
	
				except ValidationError, e:
					messages.error(request, e.message)
					trip = Trip.objects.get(pk=tripid)
			else:
				messages.error(request, trip_form.errors)
		else:
			trip_form = TripForm(instance=trip)
	except Trip.DoesNotExist:
		messages.error(request, _('You are not allowed to edit non-existing group.'))
		return HttpResponseRedirect(reverse('trips:index'))
	
	return render_to_response('trips/edit.html', {'trip': trip, 'form': trip_form}, context)

# view for display share page of the trip
@login_required
def share(request, tripid):
	context = RequestContext(request)
	user = request.user
	try:
		trip = Trip.objects.get(pk=tripid)
		if trip.owner != user:
			messages.error(request, _('You have not permission to share foreign trip.'))
			return HttpResponseRedirect(reverse('trips:index'))
	except Trip.DoesNotExist:
		messages.error(request, _('You are not allowed to share non-existing trip.'))
		return HttpResponseRedirect(reverse('trips:index'))
	
	return render_to_response('trips/share.html', {'trip': trip, 'users': trip.share_users.all(), 'groups': trip.share_groups.all(), 'user_groups': user.customgroup_set.all()}, context)

# view for handle removing user from sharing existing tripp
@login_required
def remove_user(request, tripid, userid):
	context = RequestContext(request)
	user = request.user
	try:
		trip = Trip.objects.get(pk=tripid)
		if trip.owner == user:
			deleted_user = trip.share_users.filter(id=userid).first()
			if deleted_user != None:
				trip.share_users.remove(deleted_user)
				messages.info(request, _('Successfully unshared with user ') + deleted_user.username)
			else:
				messages.error(request, _('You can not unshare trip with requested user.'))
		else:
			messages.error(request, _('You have not permission to share foreign trip.'))
	except Trip.DoesNotExist:
		messages.error(request, _('You can not share non-existing trip.'))
	
	return HttpResponseRedirect(reverse('trips:share', args=(tripid,)))

# view for handle adding user for sharing existing tripp
@login_required
def add_user(request, tripid, userid):
	context = RequestContext(request)
	user = request.user
	try:
		trip = Trip.objects.get(pk=tripid)
		if trip.owner == user:
			added_user = trip.share_users.filter(id=userid).first()
			if added_user != None:
				messages.info(request, _('This trip is already shared with user ') + added_user.username)
			else:
				try:
					added_user = User.objects.get(pk=userid)
					trip.share_users.add(added_user)
					messages.success(request, _('Successfully shared with user ') + added_user.username)
				except User.DoesNotExist:
					messages.error(request, _('You can not shared with non-existing user.'))
		else:
			messages.error(request, _('You have not permission to share foreign trip.'))
	except Trip.DoesNotExist:
		messages.error(request, _('You can not edit non-existing trip.'))
	
	return HttpResponseRedirect(reverse('trips:share', args=(tripid,)))


# view for handle removing group from sharing existing tripp
@login_required
def remove_group(request, tripid, groupid):
	context = RequestContext(request)
	user = request.user
	try:
		trip = Trip.objects.get(pk=tripid)
		if trip.owner == user:
			deleted_group = trip.share_groups.filter(id=groupid).first()
			if deleted_group != None:
				trip.share_groups.remove(deleted_group)
				messages.info(request, _('Successfully unshared with group ') + deleted_group.name)
			else:
				messages.error(request, _('You can not unshare trip with requested group.'))
		else:
			messages.error(request, _('You have not permission to share foreign trip.'))
	except Trip.DoesNotExist:
		messages.error(request, _('You can not share non-existing trip.'))
	
	return HttpResponseRedirect(reverse('trips:share', args=(tripid,)))


# view for handle adding group for sharing existing tripp
@login_required
def add_group(request, tripid, groupid):
	context = RequestContext(request)
	user = request.user
	try:
		trip = Trip.objects.get(pk=tripid)
		if trip.owner == user:
			added_group = trip.share_groups.filter(id=groupid).first()
			if added_group != None:
				messages.info(request, _('This trip is already shared with group ') + added_group.name)
			else:
				try:
					added_group = CustomGroup.objects.get(pk=groupid)
					trip.share_groups.add(added_group)
					messages.success(request, _('Successfully shared with group ') + added_group.name)
				except CustomGroup.DoesNotExist:
					messages.error(request, _('You can not shared with non-existing group.'))
		else:
			messages.error(request, _('You have not permission to share foreign trip.'))
	except Trip.DoesNotExist:
		messages.error(request, _('You can not edit non-existing trip.'))
	
	return HttpResponseRedirect(reverse('trips:share', args=(tripid,)))


# helper function, check if trip is shared with user
def __shared_trip(trip, user):
	shared_trip = (trip.owner == user) or trip.public
	shared_trip |= (user in trip.share_users.all())
	for group in trip.share_groups.all():
		shared_trip |= (user in group.users.all())
	return shared_trip
