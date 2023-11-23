# from django import forms

# from .models import Product, ProductImage

# class ProductForm(forms.ModelForm):
#     class Meta:
#         model = Product
#         fields = ['name', 'description', 'price', 'category', 'stock', 'is_active']

# class ProductImageForm(forms.ModelForm):
#     class Meta:
#         model = ProductImage
#         fields = ['image']


from django import forms
from shop.models import Coupon

class CouponForm(forms.ModelForm):
    class Meta:
        model = Coupon
        fields = ['code', 'valid_from', 'valid_till', 'discount_amount', 'min_purchase_amount', 'is_active']
        widgets = {
            'code': forms.TextInput(attrs={'class': 'form-control'}),
            'valid_from': forms.TextInput(attrs={'type': 'datetime-local', 'class': 'form-control'}),
            'valid_till': forms.TextInput(attrs={'type': 'datetime-local', 'class': 'form-control'}),
            'discount_amount': forms.NumberInput(attrs={'class': 'form-control'}),
            'min_purchase_amount': forms.NumberInput(attrs={'class': 'form-control'}),
            'is_active': forms.CheckboxInput,
        }
