from django.core.urlresolvers import reverse
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from django.shortcuts import get_object_or_404, render, render_to_response
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.http import HttpResponseRedirect, HttpResponse
from django.template.context import RequestContext
from groups.models import CustomGroup
from groups.forms import CustomGroupForm

# Create your views here.


@login_required
def index(request):
	context = RequestContext(request)
	user = request.user
	groups = user.customgroup_set.all()
	group_form = CustomGroupForm()

	return render_to_response('groups/index.html', {'groups': groups, 'form': group_form}, context)

@login_required
def create(request):
	if request.method == 'POST':
		group_form = CustomGroupForm(data=request.POST)
		if True and group_form.is_valid():
			group = group_form.save(commit=False)
			user = request.user
			group.owner = user
			try:
				group.save()
				messages.success(request, _('Successfully created group ') + group.name)
			except ValidationError, e:
				messages.error(request, e.message)
		else:
			messages.error(request, group_form.errors)
	else:
		group_form = CustomGroupForm()

	return HttpResponseRedirect(reverse('groups:index'))
