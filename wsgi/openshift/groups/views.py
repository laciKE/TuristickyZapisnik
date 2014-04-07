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

@login_required
def delete(request, groupid):
	context = RequestContext(request)
	user = request.user
	try:
		group = CustomGroup.objects.get(pk=groupid)
		if group.owner == user:
			group.delete()
			messages.info(request, _('Succesfully deleted group ') + group.name)
		else:
			messages.error(request, _('You have not permission to delete foreign group.'))
	except CustomGroup.DoesNotExist:
		messages.error(request, _('You can not delete non-existing group.'))
	
	return HttpResponseRedirect(reverse('groups:index'))

@login_required
def edit(request, groupid):
	context = RequestContext(request)
	user = request.user
	try:
		group = CustomGroup.objects.get(pk=groupid)
		if group.owner == user:
			messages.info(request, group.name)
		else:
			messages.error(request, _('You have not permission to edit foreign group.'))
	except CustomGroup.DoesNotExist:
		messages.error(request, _('You can not edit non-existing group.'))
	
	return render_to_response('groups/edit.html', {'group': group, 'users': group.users.all(), 'form': None}, context)

@login_required
def remove_user(request, groupid, userid):
	context = RequestContext(request)
	user = request.user
	try:
		group = CustomGroup.objects.get(pk=groupid)
		if group.owner == user:
			deleted_user = group.users.filter(id=userid).first()
			if deleted_user != None:
				group.users.remove(deleted_user)
				messages.error(request, _('Successfully remove user ') + deleted_user.username)
			else:
				messages.error(request, _('You can not delete non-this-group user.'))
		else:
			messages.error(request, _('You have not permission to edit foreign group.'))
	except CustomGroup.DoesNotExist:
		messages.error(request, _('You can not edit non-existing group.'))
	
	return HttpResponseRedirect(reverse('groups:edit', args=(groupid,)))
