from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User

# from django.contrib.auth.forms import UserCreationForm
# from django.contrib.auth.models import User
# from django import forms 

# class CreateUserForm(UserCreationForm) :
#     class Meta :
#         model = User
#         fields = ['first_name','last_name','username','email','password1','password2']

class UserRegisterForm(UserCreationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={"class":"form-control","placeholder": "Username"}))
    first_name = forms.CharField(widget=forms.TextInput(attrs={"class":"form-control","placeholder": "First name"}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={"class":"form-control","placeholder": "Last name"}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={"class":"form-control","placeholder": "Email Address"}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={"class":"form-control","placeholder": "Password"}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={"class":"form-control","placeholder": "Confirm-Password"}))
    mobile_number = forms.CharField(widget=forms.TextInput(attrs={"class":"form-control","placeholder": "Mobile Number"}))


    
    
    class Meta:
        model = User
        fields = ['username','first_name','last_name','email','password1','password2','mobile_number']