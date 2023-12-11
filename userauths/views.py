from imaplib import _Authenticator
import random
from django.shortcuts import render, redirect
from django.utils import timezone
from datetime import timedelta
from django.contrib.auth.hashers import make_password
from django.contrib import messages
from django.core.mail import send_mail
from .forms import UserRegisterForm
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth import authenticate,login,logout
from .models import User
from django.views.decorators.cache import never_cache


from django.contrib.auth import authenticate
from django.db.models import Q  # Import the Q object for OR queries


def send_otp(request):
    s = ""
    for x in range(0, 4):
        s += str(random.randint(0, 9))
    request.session["otp"] = s
    request.session["otp_generated_time"] = timezone.now().isoformat()
    send_mail("otp for sign up/in", s, "litleaves23@gmail.com", [request.session['email']], fail_silently=False)
        

def send_otp_password_reset(request):
    s = ""
    for x in range(0, 4):
        s += str(random.randint(0, 9))
    request.session["otp"] = s
    request.session["otp_generated_time"] = timezone.now().isoformat()
    send_mail("otp for reset password", s, "litleaves23@gmail.com", [request.session['email']], fail_silently=False)

def user_logout(request):
    logout(request)
    messages.success(request,'Logged out successfully..')
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
            request.session['first_name'] = form.cleaned_data.get('first_name') 
            request.session['last_name'] = form.cleaned_data.get('last_name')  
            request.session['mobile_number'] = form.cleaned_data.get('mobile_number')  
            send_otp(request)
            return render(request, 'userauths/otp.html', {'email': email})
    context = {
        'form': form,
    }
    return render(request, 'userauths/sign-up.html', context)

def resend_otp(request):
    send_otp(request)
    return render(request, 'userauths/otp.html')





@never_cache
def otp_verification(request):
    if request.method == 'POST':
        otp_ = request.POST.get("otp")
        
        otp_generated_time = request.session.get("otp_generated_time")

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
                return redirect('home:index') 
            else:
                messages.error(request, "OTP doesn't match")
        else:
            messages.error(request, "OTP has expired. Please request a new OTP.")
            
        return render(request, 'userauths/otp.html')
    
    
def user_sign(request):
    if request.user.is_authenticated:
        return redirect('home:index') 
    if request.method == 'POST':
        username = request.POST.get('userName')
        password = request.POST.get('password')

        user_exists = User.objects.filter(Q(username=username) | Q(email=username)).exists()
        
        if user_exists:
            user = User.objects.get(Q(username=username) | Q(email=username)) 
            if user.is_active:
                if user.check_password(password):
                    request.session['username'] = username
                    request.session['authenticated'] = True
                    request.session['email'] = user.email
                    send_otp(request) 
                    return render(request, 'userauths/otp2.html', {'email': user.email})
                else:
                    messages.error(request, 'Invalid password.')
                    return render(request, 'userauths/sign-in.html')
            else:
                messages.error(request, 'You are blocked from signing in.') 
                return render(request, 'userauths/sign-in.html')       
        else:
            messages.error(request, 'User does not exist.')
            return render(request, 'userauths/sign-in.html')

    return render(request, 'userauths/sign-in.html')


def resend_otp2(request):
    send_otp(request)
    return render(request, 'userauths/otp2.html')



def otp_verification2(request):
    if request.method == 'POST':
        otp = request.POST.get("otp")
        username = request.POST.get("username") 
        if otp == request.session.get("otp"): 
           
            username =request.session['username']
            user = User.objects.get(username=username)  
            login(request, user)

            messages.info(request, 'Signed in successfully...')
            del request.session['otp']
            del request.session['otp_generated_time']
            return redirect('home:index') 
        else:
            messages.error(request, "OTP doesn't match")
            return render(request, 'userauths/otp2.html', {'username': username})

    return render(request, 'userauths/otp2.html')
        
        
def forget_password(request):
    return render (request, 'userauths/forget_password.html')        

@never_cache
def forgot_password(request):
    if request.method == 'POST':
        email = request.POST.get('email') 
        is_email_exist = User.objects.filter(email=email).exists()

        if is_email_exist:
            request.session['email'] = email

            send_otp_password_reset(request)
            return render(request, 'userauths/paswrd_otp.html', {'email': email})        

        else:
            messages.error(request, 'Invalid Email!!')
            return redirect('userauths:forgot_password')

    return render(request,'userauths/forget_password.html')


def resend_otp3(request):
    send_otp_password_reset(request)
    return render(request, 'userauths/paswrd_otp.html')

def otp_verification_forget_password(request):
     if request.method == 'POST':
        otp_ = request.POST.get("otp")
        
        otp_generated_time = request.session.get("otp_generated_time")

        if otp_generated_time and timezone.now() - timezone.datetime.fromisoformat(otp_generated_time) < timedelta(minutes=1):
            if otp_ == request.session["otp"]:
                email = request.session['email']
                user = User.objects.get(email = email)
                return redirect('userauths:set_password')  
            else:
                messages.error(request, "OTP doesn't match")
        else:
            messages.error(request, "OTP has expired. Please request a new OTP.")
            
        return render(request, 'userauths/paswrd_otp.html')

def set_password(request):
    if request.method == 'POST':
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        
        if password1 != password2:
            messages.error(request, "Passwords do not match !!!.")
            return render(request, 'userauths/set_password.html')

        if 'email' in request.session:
            email = request.session['email']
            user = User.objects.get(email=email)

            if check_password(password1, user.password):
                messages.error(request, "New password should be different from the old password.")
                return render(request, 'userauths/set_password.html')

            user.password = make_password(password1)
            user.save()

            del request.session['email']

            messages.success(request, "Password set successfully. You can now sign in with your new password.")
            return redirect('userauths:sign-in')
        
    return render(request, 'userauths/set_password.html')
       