from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _
from django.shortcuts import get_object_or_404, render, render_to_response
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.http import HttpResponseRedirect, HttpResponse
from django.template.context import RequestContext
from groups.models import CustomGroup

# Create your views here.


@login_required
def index(request):
	context = RequestContext(request)
	user = request.user
	groups = user.customgroup_set.all()
	return render_to_response('groups/index.html', {'groups': groups}, context)

@login_required
def create(request):
	return HttpResponseRedirect(reverse('groups:index'))
