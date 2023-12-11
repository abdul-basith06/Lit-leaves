import re
from .models import *
from django import forms

  

class AddressForm(forms.ModelForm):
    class Meta:
        model = ShippingAddress  
        fields = ['full_name', 'address_lines', 'city', 'state', 'pin_code', 'country', 'mobile', 'status']   
        
    widgets = {
            'full_name': forms.TextInput(attrs={'class': 'form-control address-input'}),
            'address_lines': forms.TextInput(attrs={'class': 'form-control address-input'}),
            'city': forms.TextInput(attrs={'class': 'form-control address-input'}),
            'state': forms.TextInput(attrs={'class': 'form-control address-input'}),
            'pin_code': forms.TextInput(attrs={'class': 'form-control address-input'}),
            'country': forms.TextInput(attrs={'class': 'form-control address-input'}),
            'mobile': forms.TextInput(attrs={'class': 'form-control address-input'}),
            'status': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
    def __init__(self, *args, **kwargs):
        super(AddressForm, self).__init__(*args, **kwargs)
        self.fields['full_name'].required = True
        self.fields['pin_code'].required = True
        self.fields['mobile'].required = True
        
    def clean_mobile(self):
        mobile = self.cleaned_data.get('mobile')
        pattern = r'^[6-9]\d{9}$'
    
        if not re.match(pattern, mobile):
            raise forms.ValidationError("Enter a valid mobile number!!!")
        return mobile    
    
    def clean_pin_code(self):
        pin_code = self.cleaned_data.get('pin_code')

        if not (pin_code.isdigit() and len(pin_code) == 6):
            raise forms.ValidationError("Enter a valid 6-digit pin code!!!")

        return int(pin_code)

    
    def clean_full_name(self):
        full_name = self.cleaned_data.get('full_name')
        if not 3 <= len(full_name) <= 20:
            raise forms.ValidationError("Full name should be between 3 and 20 characters.")
        return full_name

    def clean_address_lines(self):
        address_lines = self.cleaned_data.get('address_lines')
        if len(address_lines) > 100:
            raise forms.ValidationError("Address lines should be at most 100 characters.")
        return address_lines

    def clean_city(self):
        city = self.cleaned_data.get('city')
        if len(city) > 20:
            raise forms.ValidationError("City should be at most 20 characters.")
        return city

    def clean_state(self):
        state = self.cleaned_data.get('state')
        if len(state) > 20:
            raise forms.ValidationError("State should be at most 20 characters.")
        return state

    def clean_country(self):
        country = self.cleaned_data.get('country')
        if len(country) > 20:
            raise forms.ValidationError("Country should be at most 20 characters.")
        return country