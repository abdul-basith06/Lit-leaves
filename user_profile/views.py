from django.shortcuts import redirect, render
from admin_panel.models import *
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages
from .forms import *
from shop.models import *
from .models import *
from django.http import HttpResponse  # Import HttpResponse from django.http

def dashboard(request):   
    try:
        profile = UserProfile.objects.get(user=request.user)
    except UserProfile.DoesNotExist:
        profile = None   
    context = {
        'profile' : profile,
    }
    return render(request, 'user_profile/dashboard.html', context)


def update_avatar(request):
    if request.method == 'POST':
        user_profile = UserProfile.objects.get(user=request.user)
        user_profile.dp = request.FILES['image']  # 'image' should match the input name attribute in your form
        user_profile.save()
        return redirect('user_profile:dashboard')

    return render(request, 'user_profile/dashboard.html')


def editpassword(request):
    if request.method == 'POST':
        old_password = request.POST['oldPassword']
        new_password = request.POST['newPassword']

        user = request.user

        # Check if the old password is correct
        if user.check_password(old_password):
            # Set the new password and update the session
            user.set_password(new_password)
            user.save()
            update_session_auth_hash(request, user)  # To prevent the user from being logged out

            messages.success(request, 'Password changed successfully.')
            return redirect('user_profile:dashboard')
        else:
            messages.error(request, 'Incorrect old password. Password not changed.')

    return render(request, 'user_profile/dashboard.html')  # You can change the template to where you want to redirect

def editprofile(request):
    if request.method == 'POST':
        # Retrieve the user's profile
        user_profile = UserProfile.objects.get(user=request.user)
        user = User.objects.get(pk=request.user.id)  # Retrieve the User model instance

        # Update the User model with the data from the form
        user.username = request.POST['username']
        user.first_name = request.POST['firstname']
        user.last_name = request.POST['lastname']
        user.email = request.POST['email']
        user.mobile_number = request.POST['mobile_number']
        user.save()

        # Update the UserProfile model
        user_profile.bio = request.POST.get('bio', '')
        user_profile.save()

        # Redirect to a success page or back to the profile page
        return redirect('user_profile:dashboard')
    else:
        # Handle GET requests to display the edit profile form
        return render(request, 'user_profile/editprofile.html')