from django.shortcuts import render_to_response
from django.template.context import RequestContext
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Q
from trips.models import Trip

# view for home page, simply render home template
def home(request):
	context = RequestContext(request)
	return render_to_response('home.html', {}, context)

# view for user dashboard, display list with shared trips and collect and display personal stats
@login_required
def dashboard(request):
	context = RequestContext(request)
	user = request.user
	share_trips = Trip.objects.filter(Q(share_users=user) | Q(share_groups__in=user.custom_groups.all())).distinct().order_by('-modified')

	stats = {}
	stats['last_login'] = user.last_login
	stats['date_joined'] = user.date_joined
	stats['share_trips'] = len(share_trips)
	trips = user.trip_set.all()
	stats['trips'] = len(trips)
	stats['public_trips'] = len(trips.filter(public=True))
	photos = 0
	for trip in trips:
		photos += len(trip.photo_set.all())
	stats['photos'] = photos
	stats['comments'] = len(user.comment_set.all())
	stats['groups'] = len(user.customgroup_set.all())
	stats['share_groups'] = len(user.custom_groups.all())

	return render_to_response('dashboard.html', {'trips': share_trips, 'stats': stats}, context)
