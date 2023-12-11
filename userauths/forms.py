from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User
import re



class UserRegisterForm(UserCreationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={"class":"form-control","placeholder": "Username"}))
    first_name = forms.CharField(widget=forms.TextInput(attrs={"class":"form-control","placeholder": "First name"}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={"class":"form-control","placeholder": "Last name"}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={"class":"form-control","placeholder": "Email Address"}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={"class":"form-control","placeholder": "Password"}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={"class":"form-control","placeholder": "Confirm-Password"}))
    mobile_number = forms.CharField(widget=forms.TextInput(attrs={"class":"form-control","placeholder": "Mobile Number"}))

    def clean_mobile_number(self):
        mobile_number = self.cleaned_data.get('mobile_number')
        # Define a regular expression pattern for a valid Indian mobile number (10 digits)
        pattern = r'^[6-9]\d{9}$'
    
        if not re.match(pattern, mobile_number):
            raise forms.ValidationError("Enter a valid 10 digit mobile number!!!")
        return mobile_number

    
    
    class Meta:
        model = User
        fields = ['username','first_name','last_name','email','password1','password2','mobile_number']