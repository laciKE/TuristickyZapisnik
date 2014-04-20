from django.core.urlresolvers import reverse
from django.utils import simplejson
from django.utils.translation import ugettext_lazy as _
from django.shortcuts import get_object_or_404, render, render_to_response
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.views.decorators.debug import sensitive_post_parameters
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.contrib import messages
from django.http import HttpResponseRedirect, HttpResponse, HttpResponseBadRequest, Http404
from django.template.context import RequestContext
from django.contrib.auth.forms import PasswordChangeForm
from users.forms import UserForm, UserEditForm, UserProfileForm
from trips.models import Trip

def index(request):
	context = RequestContext(request)
	return render_to_response('users/index.html', {}, context)

def profile(request, username):
	context = RequestContext(request)
	user = get_object_or_404(User, username=username)
	trips = user.trip_set.filter(public=True).order_by('-id')
	return render_to_response('users/profile.html', {'profile': user, 'trips': trips}, context)

@sensitive_post_parameters()
@csrf_protect
@never_cache
def registration(request):
    context = RequestContext(request)

    # A boolean value for telling the template whether the registration was successful.
    # Set to False initially. Code changes value to True when registration succeeds.
    registered = False

    # If it's a HTTP POST, we're interested in processing form data.
    if request.method == 'POST':
        # Attempt to grab information from the raw form information.
        # Note that we make use of both UserForm and UserProfileForm.
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileForm(data=request.POST)

        # If the two forms are valid...
        if user_form.is_valid() and profile_form.is_valid():
            # Save the user's form data to the database.
            # Since we need to set the user attribute ourselves, we set commit=False.
            # This delays saving the model until we're ready to avoid integrity problems.
 
            user = user_form.save(commit=False)

           # Now we hash the password with the set_password method.
            user.set_password(user.password)

            profile = profile_form.save(commit=False)

            # Did the user provide a profile picture?
            # If so, we need to get it from the input form and put it in the UserProfile model.
            if 'avatar' in request.FILES:
                profile.avatar = request.FILES['avatar']

            # Now we save the UserProfile and User model instance.
            user.save()
            profile.user = user
            profile.save()
            
            # Update our variable to tell the template registration was successful.
            messages.success(request, _('Registration successful, you can log in.'))
            return HttpResponseRedirect(reverse('users:login'))
 


        # Invalid form or forms - mistakes or something else?
        # Print problems to the terminal.
        # They'll also be shown to the user.
        else:
            print user_form.errors, profile_form.errors

    # Not a HTTP POST, so we render our form using two ModelForm instances.
    # These forms will be blank, ready for user input.
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()

    # Render the template depending on the context.
    return render_to_response( 'users/registration.html', {'user_form': user_form, 'profile_form': profile_form, 'registered': registered}, context)

@sensitive_post_parameters()
@csrf_protect
@never_cache
def user_login(request):
    context = RequestContext(request)

    # If the request is a HTTP POST, try to pull out the relevant information.
    if request.method == 'POST':
        # Gather the username and password provided by the user.
        # This information is obtained from the login form.
        username = request.POST['username']
        password = request.POST['password']

        # Use Django's machinery to attempt to see if the username/password
        # combination is valid - a User object is returned if it is.
        user = authenticate(username=username, password=password)

        # If we have a User object, the details are correct.
        # If None (Python's way of representing the absence of a value), no user
        # with matching credentials was found.
        if user is not None:
            # Is the account active? It could have been disabled.
            if user.is_active:
                # If the account is valid and active, we can log the user in.
                # We'll send the user back to the homepage.
                login(request, user)
                messages.success(request, _('Welcome, ') + user.username)
                return HttpResponseRedirect(reverse('dashboard'))
            else:
                # An inactive account was used - no logging in!
                messages.warning(request, _('Your account has been disabled.'))
                return render_to_response('users/login.html', {'username': username}, context)
        else:
            # Bad login details were provided. So we can't log the user in.
            messages.error(request, _('Invalid login details supplied.'))
            return render_to_response('users/login.html', {'username': username}, context)

    # The request is not a HTTP POST, so display the login form.
    # This scenario would most likely be a HTTP GET.
    else:
        # No context variables to pass to the template system, hence the
        # blank dictionary object...
        return render_to_response('users/login.html', {}, context)

@login_required
def user_logout(request):
    # Since we know the user is logged in, we can now just log them out.
    logout(request)

    messages.success(request, _('Logout successful'))

    # Take the user back to the homepage.
    return HttpResponseRedirect(reverse('home'))

@login_required
def edit(request):
    context = RequestContext(request)

    # If it's a HTTP POST, we're interested in processing form data.
    if request.method == 'POST':
        # Attempt to grab information from the raw form information.
        # Note that we make use of both UserForm and UserProfileForm.
        user_form = UserEditForm(data=request.POST, instance=request.user)
        profile_form = UserProfileForm(data=request.POST, instance=request.user.userprofile)

        # If the two forms are valid...
        if user_form.is_valid() and profile_form.is_valid():
            # Save the user's form data to the database.
            # Since we need to set the user attribute ourselves, we set commit=False.
            # This delays saving the model until we're ready to avoid integrity problems.
 
            user = user_form.save(commit=False)

            profile = profile_form.save(commit=False)

            # Did the user provide a profile picture?
            # If so, we need to get it from the input form and put it in the UserProfile model.
            if 'avatar' in request.FILES:
                profile.avatar = request.FILES['avatar']

            # Now we save the UserProfile and User model instance.
            user.save()
            profile.save()
            
            # Update our variable to tell the template registration was successful.
            messages.success(request, _('Your changes have been saved.'))
            return HttpResponseRedirect(reverse('users:profile', args=(user.username,)))
 

        # Invalid form or forms - mistakes or something else?
        # Print problems to the terminal.
        # They'll also be shown to the user.
        else:
            print user_form.errors, profile_form.errors

    # Not a HTTP POST, so we render our form using two ModelForm instances.
    # These forms will be blank, ready for user input.
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = UserProfileForm(instance=request.user.userprofile)

    # Render the template depending on the context.
    return render_to_response( 'users/edit.html', {'user_form': user_form, 'profile_form': profile_form}, context)

#from django.contrib.auth.views, modofied post_change_redirect and messages
@sensitive_post_parameters()
@csrf_protect
@login_required
def password_change(request):
    context = RequestContext(request)

    if request.method == "POST":
        form = PasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, _('Your password has been changed.'))
            return HttpResponseRedirect(reverse('users:profile', args=(request.user.username,)))
    else:
        form = PasswordChangeForm(user=request.user)
    return render_to_response( 'users/password_change.html', {'form': form,}, context)

def search(request):
	if request.method == "GET" and 'q' in request.GET:
		q = request.GET['q']
		users = User.objects.filter(username__icontains=q).filter(is_superuser=False)
		data = simplejson.dumps([(user.id, user.username, user.get_full_name(), user.userprofile.avatar.url) for user in users])
		return HttpResponse(data, mimetype='application/json')
	else:
		return HttpResponseBadRequest()
