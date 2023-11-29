from imaplib import _Authenticator
import random
from django.shortcuts import render, redirect
from django.utils import timezone
from datetime import timedelta
from django.contrib.auth.hashers import make_password
from django.contrib import messages
from django.core.mail import send_mail
from .forms import UserRegisterForm
from django.contrib.auth import authenticate,login,logout
from .models import User
from django.views.decorators.cache import never_cache


from django.contrib.auth import authenticate
from django.db.models import Q  # Import the Q object for OR queries

def user_logout(request):
    logout(request)
    return redirect('home:index')



def user_register(request):
    if request.user.is_authenticated:
        return redirect('home:index') 
    form = UserRegisterForm
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password1')
            username = form.cleaned_data.get('username')
            request.session['username'] = username
            request.session['password'] = password
            request.session['email'] = email
            request.session['first_name'] = form.cleaned_data.get('first_name')  # Added to store first_name
            request.session['last_name'] = form.cleaned_data.get('last_name')  # Added to store last_name
            request.session['mobile_number'] = form.cleaned_data.get('mobile_number')  # Added to store mobile_number
            send_otp(request)
            return render(request, 'userauths/otp.html', {'email': email})
    context = {
        'form': form,
    }
    return render(request, 'userauths/sign-up.html', context)

def resend_otp(request):
    send_otp(request)
    return render(request, 'userauths/otp.html')


def send_otp(request):
    s = ""
    for x in range(0, 4):
        s += str(random.randint(0, 9))
    request.session["otp"] = s
    request.session["otp_generated_time"] = timezone.now().isoformat()
    send_mail("otp for sign up", s, "litleaves23@gmail.com", [request.session['email']], fail_silently=False)



@never_cache
def otp_verification(request):
    if request.method == 'POST':
        otp_ = request.POST.get("otp")
        
        # Get the OTP generation time from the session
        otp_generated_time = request.session.get("otp_generated_time")

        # Check if OTP generation time exists and is within the last 1 minute
        if otp_generated_time and timezone.now() - timezone.datetime.fromisoformat(otp_generated_time) < timedelta(minutes=1):
            if otp_ == request.session["otp"]:
                encrypted_password = make_password(request.session['password'])
                user = User(
                    username=request.session['username'],
                    email=request.session['email'],
                    password=encrypted_password,
                    first_name=request.session.get("first_name"),
                    last_name=request.session.get("last_name"),
                    mobile_number=request.session.get("mobile_number")
                )
                user.save()
                login(request, user)
                messages.info(request, 'Signed in successfully...')
                user.is_active = True
                del request.session['otp']
                del request.session['otp_generated_time']
                return redirect('home:index')  # Assuming 'home:index' is the URL name for the home page
            else:
                messages.error(request, "OTP doesn't match")
        else:
            messages.error(request, "OTP has expired. Please request a new OTP.")
            
        return render(request, 'userauths/otp.html')
    
    
def user_sign(request):
    if request.user.is_authenticated:
        return redirect('home:index') 
    if request.method == 'POST':
        # Get the username and password from the form data
        username = request.POST.get('userName')
        password = request.POST.get('password')

        # Check if a user with the provided username exists
        user_exists = User.objects.filter(Q(username=username) | Q(email=username)).exists()
        
        if user_exists:
            # User exists; attempt to log in
            user = User.objects.get(Q(username=username) | Q(email=username)) 
            if user.is_active:
                if user.check_password(password):
                # Password is correct; log in the user
                    request.session['username'] = username
                    request.session['authenticated'] = True
                    # login(request, user)
                    request.session['email'] = user.email
                    send_otp(request)  # Implement the send_otp function
                    return render(request, 'userauths/otp2.html', {'email': user.email})
                else:
                    # Password is incorrect; set an error message
                    messages.error(request, 'Invalid password.')
            else:
                # User is blocked (is_active is False); set a block message
                messages.error(request, 'You are blocked from signing in.')        
        else:
            # User does not exist; set an error message
            messages.error(request, 'User does not exist.')

    # Render the sign-in form for both GET and POST requests
    return render(request, 'userauths/sign-in.html')




def otp_verification2(request):
    if request.method == 'POST':
        otp = request.POST.get("otp")
        username = request.POST.get("username")  # Get the username from the form

        if otp == request.session.get("otp"):  # Verify OTP
            # Log in the user
            username =request.session['username']
            user = User.objects.get(username=username)  # Assuming you have a User model
            login(request, user)

            messages.info(request, 'Signed in successfully...')
            del request.session['otp']
            del request.session['otp_generated_time']
            return redirect('home:index')  # Redirect to the home page after sign-in
        else:
            messages.error(request, "OTP doesn't match")
            return render(request, 'userauths/otp2.html', {'username': username})

    return render(request, 'userauths/otp2.html')
        

        
       