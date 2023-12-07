import random
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from admin_panel.models import *
from django.contrib.auth import update_session_auth_hash
from datetime import timedelta
from django.contrib.auth import logout
from django.contrib import messages
from .forms import *
from .helpers import render_to_pdf
from shop.models import *
from .models import *
from django.http import Http404, HttpResponse, JsonResponse  

@login_required
def dashboard(request):
    profile = None  
    try:
        profile = UserProfile.objects.get(user=request.user)
    except UserProfile.DoesNotExist:
        pass 
        
    customer = request.user
    order, created = Order.objects.get_or_create(customer=customer, complete=False)
    cartItems = order.get_cart_items    

    context = {
            'profile': profile,
            'cartItems':cartItems,
        }
    return render(request, 'user_profile/dashboard.html', context)

@login_required
def update_avatar(request):
    if request.method == 'POST':
        user_profile = UserProfile.objects.get(user=request.user)
        user_profile.dp = request.FILES['image'] 
        user_profile.save()
        return redirect('user_profile:dashboard')

    return render(request, 'user_profile/dashboard.html')


@login_required
def editpassword(request):
    if request.method == 'POST':
        old_password = request.POST['oldPassword']
        new_password = request.POST['newPassword']

        user = request.user

        if user.check_password(old_password):
            user.set_password(new_password)
            user.save()
            update_session_auth_hash(request, user) 
            logout(request) 
            messages.success(request, 'Password changed successfully. You have been logged out for security reasons.')
            return redirect('home:index') 
        else:
            messages.error(request, 'Incorrect old password. Password not changed.')

    return render(request, 'user_profile/dashboard.html') 

@login_required
def editprofile(request):
    if request.method == 'POST':
        user_profile = UserProfile.objects.get(user=request.user)
        user = User.objects.get(pk=request.user.id)  

        user.username = request.POST['username']
        user.first_name = request.POST['firstname']
        user.last_name = request.POST['lastname']
        user.email = request.POST['email']
        user.mobile_number = request.POST['mobile_number']
        user.save()

        user_profile.bio = request.POST.get('bio', '')
        user_profile.save()

        return redirect('user_profile:dashboard')
    else:
        return render(request, 'user_profile/editprofile.html')
    
@login_required
def all_addresses(request):
    form = AddressForm()
    all_address = ShippingAddress.objects.filter(user=request.user)
    
    has_default_address = any(all_address.status for all_address in all_address)

    if not has_default_address and all_address:
        all_address[0].status = True
        all_address[0].save()
        
    customer = request.user
    order, created = Order.objects.get_or_create(customer=customer, complete=False)
    cartItems = order.get_cart_items      
        
    context = {
        'address' : all_address,
        'form':form,
        'cartItems':cartItems,
    }
    return render(request, 'user_profile/all-addresses.html', context)   
 
 
@login_required
def add_address(request):
    form = AddressForm() 
    if request.method == 'POST':
        form = AddressForm(request.POST)
        if form.is_valid():
            print("Form is valid")
            new_address = form.save(commit=False)
            new_address.user = request.user
            new_address.save()
            if form.cleaned_data.get('status', False):
                ShippingAddress.objects.filter(user=request.user).exclude(id=new_address.id).update(status=False)
            print("Redirecting to all addresses")
            return redirect('user_profile:all_addresses')
        else:
            print("Form is not valid")
    else:
        form = AddressForm()

    context = {
        'form': form
    }
    return render(request, 'user_profile/all-addresses.html', context)


@login_required
def edit_address(request, address_id):
    address = get_object_or_404(ShippingAddress, id=address_id)

    form = AddressForm(instance=address)

    context = {
        'form': form,
        'address_id': address_id,
    }

    return render(request, 'user_profile/edit-address.html', context)

@login_required
def update_address(request, address_id):
    up_address = get_object_or_404(ShippingAddress, id=address_id)

    if request.method == 'POST':
        form = AddressForm(request.POST, instance=up_address)
        if form.is_valid():
            form.save()
            if form.cleaned_data.get('status', False):
                ShippingAddress.objects.exclude(id=up_address.id).update(status=False)
            return redirect('user_profile:all_addresses')
    else:
        form = AddressForm(instance=up_address)

    context = {
        'form': form,
        'address_id': address_id,
    }

    return render(request, 'user_profile/edit-address.html', context)

@login_required
def delete_address(request, address_id):
    address_del = get_object_or_404(ShippingAddress, id=address_id)

    if request.method == 'POST':
        address_del.delete()
        return redirect('user_profile:all_addresses')

    return render(request, 'user_profile/all-addresses.html')


@login_required
def my_orders(request):
    orders = Order.objects.filter(customer=request.user, complete=True).prefetch_related('orderitem_set__product')

    for order in orders:
        order.expected_delivery_date = order.date_ordered + timedelta(days=3)
        order.seven_days_after_delivery = order.expected_delivery_date + timedelta(days=7)
        
    customer = request.user
    order, created = Order.objects.get_or_create(customer=customer, complete=False)
    cartItems = order.get_cart_items      

    context = {
        'orders':orders,
        'cartItems':cartItems,
    }
    return render(request, 'user_profile/my-orders.html', context)

@login_required
def cancel_order(request, order_item_id):
    order_item = get_object_or_404(OrderItem, id=order_item_id)
    
    order_item.variation.stock += order_item.quantity
    order_item.variation.save() 
    
    
    order_item.delivery_status = 'CN'
    order_item.save()
    
    if order_item.order.payment_method == 'RAZ' or order_item.order.payment_method == 'WAL':
        user_wallet = Wallet.objects.get(user=request.user)
        total_amount = order_item.get_total() if callable(order_item.get_total) else order_item.get_total  
        user_wallet.balance += total_amount
        user_wallet.save()
    
    messages.success(request, 'Order canceled successfully.')
    return redirect('user_profile:my_orders')

@login_required
def return_order(request, order_item_id):
    order_item = get_object_or_404(OrderItem, id=order_item_id)
    
    try:
        order_item.delivery_status = 'RT'
        order_item.save()
        
        order_item.variation.stock += order_item.quantity
        order_item.variation.save() 
        
        user_wallet = Wallet.objects.get(user=request.user)
        total_amount = order_item.get_total() if callable(order_item.get_total) else order_item.get_total  
        user_wallet.balance += total_amount
        user_wallet.save()

        messages.success(request, 'Return Item request success.')
    except Exception as e:
        messages.error(request, f'Error processing return request: {e}')
    return redirect('user_profile:my_orders')


@login_required
def wallet(request):
    user_wallet = None
    if request.user.is_authenticated:
        user_wallet = Wallet.objects.get(user=request.user)
        
    customer = request.user
    order, created = Order.objects.get_or_create(customer=customer, complete=False)
    cartItems = order.get_cart_items  
        
    context = {
        'user_wallet': user_wallet,
        'cartItems':cartItems,
    }
    return render(request, 'user_profile/wallet.html', context)

@login_required
def coupons(request):
    all_coupons = Coupon.objects.all()
    eligible_coupons = []
    used_coupons = []
    expired_coupons = []
    current_date = timezone.now().date()
    print(current_date)

    for coupon in all_coupons:
        if coupon.valid_till.date() < current_date:
            expired_coupons.append(coupon)
        elif coupon.is_user_eligible(request.user):
            eligible_coupons.append(coupon)
        else:
            used_coupons.append(coupon)
              
    customer = request.user
    order, created = Order.objects.get_or_create(customer=customer, complete=False)
    cartItems = order.get_cart_items  
              
    context = {
        'eligible_coupons': eligible_coupons,
        'used_coupons': used_coupons,
        'expired_coupons': expired_coupons,
        'cartItems':cartItems,

    }
    return render(request, 'user_profile/coupon.html', context)

@login_required
def wishlist(request):
    wishlist = Wishlist.objects.get(user=request.user)
    customer = request.user
    order, created = Order.objects.get_or_create(customer=customer, complete=False)
    cartItems = order.get_cart_items
    context = {
        'wishlist':wishlist,
        'cartItems':cartItems,
    }
    return render(request, 'user_profile/wishlist.html',context)

@login_required
def remove_item_wishlist(request, item_id):
    wishlist = get_object_or_404(Wishlist, user=request.user)
    product = get_object_or_404(Product, id=item_id)

    wishlist.items.remove(product)
    wishlist.save()
    
    return redirect('user_profile:wishlist')

@login_required
def add_to_wishlist(request, product_id):
    response_data = {}
    try:
        if not request.user.is_authenticated:
            raise Exception('User not authenticated')

        wishlist = Wishlist.objects.get(user=request.user)
        product = get_object_or_404(Product, id=product_id)

        if product in wishlist.items.all():
            # Item is already in the wishlist
            response_data['success'] = False
            response_data['message'] = 'Item is already in your wishlist'
        else:
            wishlist.items.add(product)
            wishlist.save()
            response_data['success'] = True
            response_data['message'] = 'Item added to your wishlist'
    except Exception as e:
        response_data['success'] = False
        response_data['error'] = str(e)
    return JsonResponse(response_data, safe=False)

@login_required
def generate_invoice(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    invoice_number = str(random.randint(100000, 999999))

    context = {
        'order': order,
        'invoice_number':invoice_number,
       
    }

    pdf = render_to_pdf('user_profile/invoice.html', context)
    if pdf:
        response = HttpResponse(pdf, content_type='application/pdf')
        filename =f"invoice_{order.id}.pdf"
        content = "inline; filename='%s'" % filename
        response['Content-Disposition'] = content
        return response
    else:
        print("Error generating the PDF.")
        return HttpResponse("Error generating the invoice.")

    