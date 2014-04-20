from django.shortcuts import render_to_response
from django.template.context import RequestContext
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Q
from trips.models import Trip

def home(request):
	context = RequestContext(request)
	return render_to_response('home.html', {}, context)

@login_required
def dashboard(request):
	context = RequestContext(request)
	user = request.user
	trips = Trip.objects.filter(Q(share_users=user) | Q(share_groups__in=user.custom_groups.all()))
	return render_to_response('dashboard.html', {'trips': trips}, context)
