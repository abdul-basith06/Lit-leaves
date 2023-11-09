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