import json
from django.http import HttpResponse, JsonResponse
from django.core.exceptions import ObjectDoesNotExist 
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from .models import *
from django.urls import reverse
from django.db import transaction
from user_profile.models import *
from django.db import transaction
from imaplib import _Authenticator
import random
import razorpay
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


def store(request, category_slug=None):
    cartItems = None 
    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
        
    category_id = request.GET.get('category')
    categories = Categories.objects.all()    
    selected_category_ids = request.GET.getlist('categories')
    if category_id:
        products = Product.objects.filter(category__id=category_id, is_active=True)
    else:
         products = Product.objects.filter(is_active=True)

    if selected_category_ids:
        category_filters = [Q(category__id=cat_id) for cat_id in selected_category_ids]
        combined_category_filter = Q()
        for category_filter in category_filters:
            combined_category_filter |= category_filter
        products = products.filter(combined_category_filter)
            
    min_price = request.GET.get('min_price', None)
    max_price = request.GET.get('max_price', None)  
        
    if min_price and max_price:
        try:
            min_price = float(min_price)
            max_price = float(max_price)
            products = products.filter(price__range=(min_price, max_price))
        except ValueError:
            pass         
    
    new_product_threshold = timezone.now() - timedelta(days=1)

    for product in products:
        product.variation = product.productlanguagevariation_set.first()
        product.is_new = product.date_added >= new_product_threshold and product.date_added < timezone.now()

        
        

    paginator = Paginator(products, 9)
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
        'categories': categories,
        'selected_category_ids': selected_category_ids,
        'min_price': min_price,
        'max_price': max_price,
    }    
    

    return render(request, 'shop/store.html', context)


def get_variation_stock(request, variation_id):
    try:
        variation = ProductLanguageVariation.objects.get(id=variation_id)
        stock = variation.stock
        return JsonResponse({'stock': stock})
    except ProductLanguageVariation.DoesNotExist:
        return JsonResponse({'stock': 0})


def product(request, product_id):
    items = None
    cartItems = None
    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    selected_product = Product.objects.get(pk=product_id)
    category = selected_product.category
    variations = selected_product.productlanguagevariation_set.all()
    
    
    selected_variation_id = request.GET.get('selected_variation_id')
    selected_variation = None

    if selected_variation_id:
        try:
            selected_variation = ProductLanguageVariation.objects.get(id=selected_variation_id)
        except ProductLanguageVariation.DoesNotExist:
            selected_variation = None
    
    related_products = Product.objects.filter(category=category).exclude(pk=selected_product.id)[:4]
    is_in_cart = False

    if items: 
        for item in items:
            if item.product.id == selected_product.id:
                is_in_cart = True
                break
            
    related_products_in_cart = []

    if items: 
        for related_product in related_products:
            for item in items:
                if item.product.id == related_product.id:
                    related_products_in_cart.append(related_product)
                    break 
    context = {
        'product': selected_product,
        'related_products': related_products,
        'variations' : variations,
        'cartItems': cartItems,
        'is_in_cart': is_in_cart,
        'related_products_in_cart': related_products_in_cart,
        'selected_variation': selected_variation,
    }

    return render(request, 'shop/product.html', context)


@login_required(login_url='userauths:sign-in')
def cart(request):
    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all() 
        cartItems = order.get_cart_items
        order.applied_coupon = None
        order.save()
        context = {
            'items' : items,
            'order' : order,
            'cartItems': cartItems,
        }

    return render(request, 'shop/cart.html', context)




# @login_required(login_url='userauths:sign-in')
@transaction.atomic    
def updateItem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']
    selectedVariationId = data['selectedVariationId']
    print('Action:', action)
    print('productId:', productId)
    print('selectedVariationId:', selectedVariationId)
    
    
    customer = request.user
    product = Product.objects.get(pk=productId)
    order, created = Order.objects.get_or_create(customer=customer, complete=False)
    
    
    if not selectedVariationId:
        return JsonResponse({"error": "No variation selected"}, status=400)
    try:
        selected_variation = ProductLanguageVariation.objects.get(id=selectedVariationId)
    except ProductLanguageVariation.DoesNotExist:
        return JsonResponse({"error": "Selected variation does not exist"}, status=400)

    if selected_variation.stock <= 0:
        return JsonResponse({"error": "Selected variation is out of stock"}, status=400)
    
    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product, variation=selected_variation)
    if action == 'add':
        if selected_variation.stock > 0:
            orderItem.quantity += 1
            selected_variation.stock -= 1
            selected_variation.save()
        else:
            return JsonResponse("Item quantity exceeds available stock", status=400)
    elif action == 'remove':
        if orderItem.quantity > 0:
            orderItem.quantity -= 1
            selected_variation.stock += 1
            selected_variation.save()
        else:
            return JsonResponse("Item quantity cannot be negative", status=400)

    orderItem.save()

    if orderItem.quantity <= 0:
        orderItem.delete()

    return JsonResponse("Item was added", safe=False)
    
    


@transaction.atomic
def clearItem(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            data = json.loads(request.body)
            productId = data['productId']
            variationId = data['variationId']  # Get the variation ID from the data

            customer = request.user
            order, created = Order.objects.get_or_create(customer=customer, complete=False)

            product = Product.objects.get(pk=productId)

            try:
                orderItem = OrderItem.objects.get(order=order, product=product, variation=variationId)  # Use variation ID in the query

                # Update variation stock here
                selected_variation = ProductLanguageVariation.objects.get(id=variationId)
                selected_variation.stock += orderItem.quantity
                selected_variation.save()

                orderItem.delete()
                return JsonResponse("Item was removed from the cart", safe=False)

            except OrderItem.DoesNotExist:
                return JsonResponse("Item not found in the cart", safe=False)

    return JsonResponse("You must be logged in to perform this action", status=400)    
  
  
@login_required(login_url='userauths:sign-in')  
def checkout(request):
    if request.user.is_authenticated:
        customer = request.user
        
        order = Order.objects.filter(customer=customer, complete=False).first()
        
        if not order:
            order = Order.objects.create(customer=customer)
         
        order.applied_coupon = None
        order.save()
        items = order.orderitem_set.all() 
        cartItems = order.get_cart_items
        address = ShippingAddress.objects.filter(user=customer)
        default_address = ShippingAddress.objects.filter(user=customer, status=True).first()
        remaining_addresses = ShippingAddress.objects.filter(user=customer, status=False)
        user_wallet = Wallet.objects.get(user=customer)
        
    user_info = {
        "name": request.user.get_full_name(),
        "email": request.user.email,
        "contact": request.user.mobile_number,
    }
        
       
        
    context = {
        'address' : address,
        'items' : items,
        'order' : order,
        'cartItems': cartItems,
        'da':default_address,
        'ra' : remaining_addresses,
        'user_info':user_info,
        'user_wallet':user_wallet,
        # 'cur_order':cur_order,
    }
    return render(request, 'shop/checkout.html', context)

@login_required(login_url='userauths:sign-in')
def apply_coupon(request, order_id):
    cart = get_object_or_404(Order, id=order_id)
    
    if request.method == 'POST':
        coupon_code = request.POST.get('coupon')
        try:
            coupon = Coupon.objects.get(code=coupon_code)
            
            if coupon.valid_till < timezone.now():
                messages.error(request, 'Coupon has expired.', extra_tags='danger')
            elif cart.get_cart_total < coupon.min_purchase_amount:
                messages.error(request, f'Amount should be greater than {coupon.min_purchase_amount}', extra_tags='danger')
            elif not coupon.is_user_eligible(request.user):
                messages.error(request, 'You have already used this coupon.', extra_tags='danger')
            elif cart.applied_coupon:
                messages.error(request, 'Coupon already applied.', extra_tags='danger')
            else:
                cart.applied_coupon = coupon
                cart.save()
                messages.success(request, 'Coupon successfully applied.', extra_tags='success')

        except Coupon.DoesNotExist:
            messages.error(request, 'Invalid coupon code. Please try again.', extra_tags='danger')

    items = cart.orderitem_set.all() 
    cart_items = cart.get_cart_items
    address = ShippingAddress.objects.filter(user=request.user)
    default_address = ShippingAddress.objects.filter(user=request.user, status=True).first()
    remaining_addresses = ShippingAddress.objects.filter(user=request.user, status=False)
    user_wallet = Wallet.objects.get(user=request.user)

    user_info = {
        "name": request.user.get_full_name(),
        "email": request.user.email,
        "contact": request.user.mobile_number,
    }

    context = {
        'address': address,
        'items': items,
        'order': cart,
        'cartItems': cart_items,
        'da': default_address,
        'ra': remaining_addresses,
        'user_info': user_info,
        'user_wallet': user_wallet,
    }

    return render(request, 'shop/checkout.html', context)
   
@login_required(login_url='userauths:sign-in')
def remove_coupon(request, order_id):
    order = get_object_or_404(Order, id=order_id)

    if order.applied_coupon:
        order.applied_coupon.used_by.remove(request.user)
        order.applied_coupon = None
        order.save()
        messages.success(request, 'Coupon removed successfully.', extra_tags='success')
    else:
        messages.error(request, 'No coupon to remove.', extra_tags='danger')

    items = order.orderitem_set.all() 
    cart_items = order.get_cart_items 
    address = ShippingAddress.objects.filter(user=request.user)
    default_address = ShippingAddress.objects.filter(user=request.user, status=True).first()
    remaining_addresses = ShippingAddress.objects.filter(user=request.user, status=False)
    user_wallet = Wallet.objects.get(user=request.user)

    user_info = {
        "name": request.user.get_full_name(),
        "email": request.user.email,
        "contact": request.user.mobile_number,
    }

    context = {
        'address': address,
        'items': items,
        'order': order,
        'cartItems': cart_items,
        'da': default_address,
        'ra': remaining_addresses,
        'user_info': user_info,
        'user_wallet': user_wallet,
    }

    return render(request, 'shop/checkout.html', context)

@login_required(login_url='userauths:sign-in')
@transaction.atomic
def place_order(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            selected_payment_method = request.POST.get('payment_method')
            selected_address_id = request.POST.get('selected_address')
            order_notes = request.POST.get('order_notes')
            
            try:
                selected_address = ShippingAddress.objects.get(id=selected_address_id)
            except ShippingAddress.DoesNotExist:
                messages.error(request, "Please select a valid shipping address before placing your order.")
                return redirect('shop:checkout') 

            cart_items = OrderItem.objects.filter(order__customer=request.user, order__complete=False)
            if not cart_items:
                messages.error(request, "Your cart is empty. Add items to your cart before placing an order.")
                return redirect('shop:cart')
                       
            order = Order(
                customer=request.user, 
                order_notes=order_notes,
                shipping_address=selected_address,
                
            )
            
            current_cart = Order.objects.select_for_update().get(customer=request.user, complete=False)
            if current_cart.applied_coupon:
                order.applied_coupon = current_cart.applied_coupon
            print('Applied Coupon:', order.applied_coupon)
            order.save()
            
            if selected_payment_method == 'cod':
                order.payment_method='COD'
            elif selected_payment_method == 'wallet':
                order.payment_method='WAL'
                user_wallet = Wallet.objects.get(user=request.user)
                if order.applied_coupon:
                    total_amount = sum(cart_item.get_total() if callable(cart_item.get_total) else cart_item.get_total  for cart_item in cart_items)
                    total_amount -= order.applied_coupon.discount_amount
                    user_wallet.balance -= total_amount
                    user_wallet.save()
                else:
                    total_amount = sum(cart_item.get_total() if callable(cart_item.get_total) else cart_item.get_total  for cart_item in cart_items)
                    user_wallet.balance -= total_amount
                    user_wallet.save()
                        
                if order.applied_coupon:
                    order.applied_coupon.mark_as_used(request.user)    
                
                
            order.complete = True
            order.save()
           
            for cart_item in cart_items:
                cart_item.order = order 
                cart_item.delivery_status = 'PL'
                cart_item.save()
           
            messages.success(request, 'Your order has been placed successfully!')                
            return redirect('shop:orderplaced')
    return render(request, "checkout.html")


@login_required(login_url='userauths:sign-in')
@transaction.atomic
def place_order_razorpay(request):
    if request.method == 'POST':
        selected_address_id = request.POST.get('selectedAddressId')
        order_notes = request.POST.get('orderNotes')
        transaction_id = request.POST.get('transaction_id')

        try:
            selected_address = ShippingAddress.objects.get(id=selected_address_id)
        except ShippingAddress.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Invalid shipping address'})

        order = Order(
            customer=request.user,
            payment_method='RAZ',
            order_notes=order_notes,
            shipping_address=selected_address,
            transaction_id=transaction_id
        )
        current_cart = Order.objects.select_for_update().get(customer=request.user, complete=False)
        if current_cart.applied_coupon:
            order.applied_coupon = current_cart.applied_coupon
        order.save()
        if order.applied_coupon:
            order.applied_coupon.mark_as_used(request.user)   

        order.complete = True
        order.save()

        cart_items = OrderItem.objects.filter(order__customer=request.user, order__complete=False)
        for cart_item in cart_items:
            cart_item.order = order
            cart_item.delivery_status = 'PL'
            cart_item.save()
            
        cart_items.delete()

        return JsonResponse({'status': 'success', 'message': 'Your order has been placed successfully!'})

    return JsonResponse({'status': 'error', 'message': 'Invalid request method'})



@login_required(login_url='userauths:sign-in')
def proceed_to_pay(request):
    cart = Order.objects.filter(customer=request.user, complete=False).first()
    total_price = cart.get_cart_total
    
    
    return JsonResponse({
        'total_price':total_price,
        
    })
    
@login_required(login_url='userauths:sign-in')    
def order_placed_view(request):
    return render(request, 'shop/orderplaced.html')    
    
    
@login_required(login_url='userauths:sign-in')    
def change_address(request, address_id):  
    selected_address = get_object_or_404(ShippingAddress, id=address_id, user=request.user)
 
    selected_address.status = True
    selected_address.save()

    ShippingAddress.objects.filter(user=request.user).exclude(id=address_id).update(status=False)

    return redirect('shop:checkout')

@login_required(login_url='userauths:sign-in')
def addaddress(request):
    return render(request, 'shop/addaddress.html')


@login_required(login_url='userauths:sign-in')
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

        
        if status:
            ShippingAddress.objects.filter(user=user).exclude(id=address.id).update(status=False)
            address.status = True
            address.save()
        
        
        messages.success(request, 'Address added successfully.')
        return redirect('shop:checkout')

    return render(request, 'addaddress.html')

def generate_transaction_id():
    return random.randint(1000000000, 9999999999)