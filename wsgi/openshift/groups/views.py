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
from groups.forms import CustomGroupForm

# view for display form for create new group and list of user's groups
@csrf_protect
@login_required
def index(request):
	context = RequestContext(request)
	user = request.user
	groups = user.customgroup_set.all()
	group_form = CustomGroupForm()
	return render_to_response('groups/index.html', {'groups': groups, 'form': group_form}, context)

# view for handle creation of new group
@csrf_protect
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

# view for handle deletion of existing group (also checks validity of such a request, e.g requested user is owner of group)
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

# view for display editation page of existing group. Also checks validity of such a request
@login_required
def edit(request, groupid):
	context = RequestContext(request)
	user = request.user
	try:
		group = CustomGroup.objects.get(pk=groupid)
		if group.owner != user:
			messages.error(request, _('You have not permission to edit foreign group.'))
			return HttpResponseRedirect(reverse('groups:index'))
	except CustomGroup.DoesNotExist:
		messages.error(request, _('You are not allowed to edit non-existing group.'))
		return HttpResponseRedirect(reverse('groups:index'))
	
	return render_to_response('groups/edit.html', {'group': group, 'users': group.users.all(), 'form': None}, context)

# view for handle removing user from existing group. Also checks validity of such a request
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
				messages.info(request, _('Successfully removed user ') + deleted_user.username)
			else:
				messages.error(request, _('You can not delete non-this-group user.'))
		else:
			messages.error(request, _('You have not permission to edit foreign group.'))
	except CustomGroup.DoesNotExist:
		messages.error(request, _('You can not edit non-existing group.'))
	
	return HttpResponseRedirect(reverse('groups:edit', args=(groupid,)))

# view for handle adding user to existing group. Also checks validity of such a request
@login_required
def add_user(request, groupid, userid):
	context = RequestContext(request)
	user = request.user
	try:
		group = CustomGroup.objects.get(pk=groupid)
		if group.owner == user:
			added_user = group.users.filter(id=userid).first()
			if added_user != None:
				messages.info(request, _('Already in this group: user ') + added_user.username)
			else:
				try:
					added_user = User.objects.get(pk=userid)
					group.users.add(added_user)
					messages.success(request, _('Successfully added user ') + added_user.username)
				except User.DoesNotExist:
					messages.error(request, _('You can not add non-existing user.'))
		else:
			messages.error(request, _('You have not permission to edit foreign group.'))
	except CustomGroup.DoesNotExist:
		messages.error(request, _('You can not edit non-existing group.'))
	
	return HttpResponseRedirect(reverse('groups:edit', args=(groupid,)))
