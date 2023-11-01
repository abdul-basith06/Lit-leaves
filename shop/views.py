import json
from django.http import JsonResponse
from .models import *
from imaplib import _Authenticator
import random
from django.shortcuts import render, redirect
from django.utils import timezone
from datetime import timedelta
from django.contrib.auth.hashers import make_password
from django.contrib import messages
from django.core.mail import send_mail
from django.contrib.auth import authenticate,login,logout
from .models import User
from django.views.decorators.cache import never_cache
from django.shortcuts import render
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from admin_panel.models import *

from django.shortcuts import render, get_object_or_404


# Create your views here.



def store(request):
    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    products = Product.objects.filter(is_active=True)  # Fetch only active products
    paginator = Paginator(products, 9)  # Show 9 active products per page

    page = request.GET.get('page')
    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        products = paginator.page(1)
    except EmptyPage:
        products = paginator.page(paginator.num_pages)
        
    context = {
        'products': products,
        'cartItems': cartItems,
    }    

    return render(request, 'shop/store.html', context)




def product(request, product_id):
    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    selected_product = Product.objects.get(pk=product_id)
    category = selected_product.category

    # Query related products from the same category, excluding the selected product
    related_products = Product.objects.filter(category=category).exclude(pk=selected_product.id)[:4]

    context = {
        'product': selected_product,
        'related_products': related_products,
        'cartItems': cartItems,
    }

    return render(request, 'shop/product.html', context)




def cart(request):
    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()  # Correctly access order items
        cartItems = order.get_cart_items
        context = {
            'items' : items,
            'order' : order,
            'cartItems': cartItems,
        }

    return render(request, 'shop/cart.html', context)
    
def updateItem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']
    print('Action:',action)
    print('productId:',productId)
    
    customer = request.user
    product = Product.objects.get(pk=productId)
    order, created = Order.objects.get_or_create(customer=customer, complete=False)
    
    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)
    if action == 'add':
        orderItem.quantity += 1
    elif action == 'remove':
         orderItem.quantity -= 1
         
    orderItem.save()     
    
    if orderItem.quantity <= 0:
        orderItem.delete() 
        
    return JsonResponse("Item was added", safe=False)
#  return render(request, 'shop/maanyam.html')
  
  

