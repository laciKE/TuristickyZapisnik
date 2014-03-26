from django.shortcuts import render
from users.forms import UserForm, UserProfileForm
import Image
# Create your views here.

def registration(request):
#    context = RequestContext(request)

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
                profile_avatar = request.FILES['avatar']

            # Now we save the UserProfile and User model instance.
            user.save()
            profile.user = user
            profile.save()
            
            # Update our variable to tell the template registration was successful.
            registered = True

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
    return render(request, 'users/registration.html', {'user_form': user_form, 'profile_form': profile_form, 'registered': registered})
