import json
from django.http import JsonResponse
from .models import *
from user_profile.models import *
from django.db import transaction
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
    
    for product in products:
        product.in_cart = any(item.product == product for item in items)

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

    
    related_products = Product.objects.filter(category=category).exclude(pk=selected_product.id)[:4]
    is_in_cart = False
    for item in items:
        if item.product.id == selected_product.id:
            is_in_cart = True
            break
    related_products_in_cart = []
    for related_product in related_products:
        for item in items:
            if item.product.id == related_product.id:
                related_products_in_cart.append(related_product)
                break    
    context = {
        'product': selected_product,
        'related_products': related_products,
        'cartItems': cartItems,
        'is_in_cart': is_in_cart,
        'related_products_in_cart': related_products_in_cart,
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
    
@transaction.atomic    
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
            product.stock -= 1
    elif action == 'remove':
        orderItem.quantity -= 1
        product.stock += 1
         
    orderItem.save()   
    product.save()  
    
    if orderItem.quantity <= 0:
        orderItem.delete() 
        
    return JsonResponse("Item was added", safe=False)

  
  

def clearItem(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            data = json.loads(request.body)
            productId = data['productId']

            # Fetch the user's cart
            customer = request.user
            order, created = Order.objects.get_or_create(customer=customer, complete=False)

            # Get the specific item to be removed
            product = Product.objects.get(pk=productId)

            # Check if the item exists in the cart
            try:
                orderItem = OrderItem.objects.get(order=order, product=product)

                product.stock += orderItem.quantity
                product.save()
                orderItem.delete()
                return JsonResponse("Item was removed from the cart", safe=False)

            except OrderItem.DoesNotExist:
                return JsonResponse("Item not found in the cart", safe=False)

    return JsonResponse("You must be logged in to perform this action", safe=False)
  
  
def checkout(request):
    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()  # Correctly access order items
        cartItems = order.get_cart_items
        address = ShippingAddress.objects.filter(user=customer)
        context = {
            'address' : address,
            'items' : items,
            'order' : order,
            'cartItems': cartItems,
        }
    return render(request, 'shop/checkout.html', context)


def addaddress(request):

    return render(request, 'shop/addaddress.html')


def update_address(request):
    if request.method == 'POST':
        full_name = request.POST.get('full_name')
        address_line = request.POST.get('address_line')
        city = request.POST.get('city')
        state = request.POST.get('state')
        pin_code = request.POST.get('pin_code')
        country = request.POST.get('country')
        mobile = request.POST.get('mobile')
        status = request.POST.get('status') == 'on'

        
        user = request.user  
        address = ShippingAddress(
            user=user,
            full_name=full_name,
            address_lines=address_line,
            city=city,
            state=state,
            pin_code=pin_code,
            country=country,
            mobile=mobile,
            status=status
        )
        address.save()
        messages.success(request, 'Address added successfully.')

        return redirect('shop:checkout')

    return render(request, 'addaddress.html')

def generate_transaction_id():
    return random.randint(1000000000, 9999999999)

def place_order(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            # Get form data
            selected_address_id = request.POST.get('selected_address')
            order_notes = request.POST.get('order_notes')
            selected_address = ShippingAddress.objects.get(id=selected_address_id)

            # Generate a transaction ID (you can customize this part)
            transaction_id = generate_transaction_id()

            # Create the order
            order = Order(
                customer=request.user,  # Assuming you have an authenticated user
                payment_method='COD',  # Change this to the actual payment method
                order_notes=order_notes,
                shipping_address=selected_address,
                transaction_id=transaction_id
            )
            cart_items = OrderItem.objects.filter(order__customer=request.user, order__complete=False)
            order.save()
            order.complete = True
            order.save()
            
            # Move cart items to the new order
            for cart_item in cart_items:
                cart_item.order = order  # Change the order to the new one
                cart_item.save()
           
            messages.success(request, 'Your order has been placed successfully!')
            return redirect('shop:orderplaced')

    return render(request, "checkout.html")

def order_placed_view(request):
    return render(request, 'shop/orderplaced.html')

# def place_order(request):
#     if request.user.is_authenticated:
#         if request.method == 'POST':
#         # Get form data
#             selected_address_id = request.POST.get('selected_address')
#             order_notes = request.POST.get('order_notes')
#             selected_address = ShippingAddress.objects.get(id=selected_address_id)

#         # Generate a transaction ID (you can customize this part)
#             transaction_id = generate_transaction_id()

#         # Create the order
#             order = Order(
#                 customer=request.user,  # Assuming you have an authenticated user
#             # Use the selected_address here if you have an Address model
#                 payment_method='COD',  # Change this to the actual payment method
#                 order_notes=order_notes,
#                 shipping_address=selected_address,
#                 transaction_id=transaction_id
#             # You may need to set other fields here
#             )
#             order.save()
#             order.complete = True
#             order.save()
            
#             cart_items =OrderItem.objects.filter(order=order)
            
#             for cart_item in cart_items:
#                 order_item = OrderItem(
#                     product=cart_item.product,
#                     order=order,
#                     quantity=cart_item.quantity
#                 )
#                 order_item.save()

#             # Clear the user's cart (you need to implement this part)
#             OrderItem.objects.filter(order=order).delete()

#         # Optionally, you can add the ordered items to the order here

#         # After creating the order, you can display a success message or redirect to an order summary page
#             messages.success(request, 'Your order has been placed successfully!')
#             return redirect('shop:store')  # Redirect to the order summary page
   

#     return render(request, "checkout.html")
