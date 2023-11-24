from django.shortcuts import get_object_or_404, redirect, render
from admin_panel.models import *
from django.contrib.auth import update_session_auth_hash
from datetime import timedelta
from django.contrib import messages
from .forms import *
from shop.models import *
from .models import *
from django.http import Http404, HttpResponse, JsonResponse  # Import HttpResponse from django.http

def dashboard(request):
    if request.user.is_authenticated:
        profile = None  # Initialize to None to handle exceptions
        try:
            profile = UserProfile.objects.get(user=request.user)
        except UserProfile.DoesNotExist:
            pass  # Handle the case when the profile does not exist

        context = {
            'profile': profile,
        }
        return render(request, 'user_profile/dashboard.html', context)

    raise Http404("User is not authenticated")  # Handle the case when the user is not authenticated


def update_avatar(request):
    if request.method == 'POST':
        user_profile = UserProfile.objects.get(user=request.user)
        user_profile.dp = request.FILES['image']  # 'image' should match the input name attribute in your form
        user_profile.save()
        return redirect('user_profile:dashboard')

    return render(request, 'user_profile/dashboard.html')



def editpassword(request):
    if request.method == 'POST':
        old_password = request.POST['oldPassword']
        new_password = request.POST['newPassword']

        user = request.user

        # Check if the old password is correct
        if user.check_password(old_password):
            # Set the new password and update the session
            user.set_password(new_password)
            user.save()
            update_session_auth_hash(request, user)  # To prevent the user from being logged out

            messages.success(request, 'Password changed successfully.')
            return redirect('user_profile:dashboard')
        else:
            messages.error(request, 'Incorrect old password. Password not changed.')

    return render(request, 'user_profile/dashboard.html')  # You can change the template to where you want to redirect

def editprofile(request):
    if request.method == 'POST':
        # Retrieve the user's profile
        user_profile = UserProfile.objects.get(user=request.user)
        user = User.objects.get(pk=request.user.id)  # Retrieve the User model instance

        # Update the User model with the data from the form
        user.username = request.POST['username']
        user.first_name = request.POST['firstname']
        user.last_name = request.POST['lastname']
        user.email = request.POST['email']
        user.mobile_number = request.POST['mobile_number']
        user.save()

        # Update the UserProfile model
        user_profile.bio = request.POST.get('bio', '')
        user_profile.save()

        # Redirect to a success page or back to the profile page
        return redirect('user_profile:dashboard')
    else:
        # Handle GET requests to display the edit profile form
        return render(request, 'user_profile/editprofile.html')
    

def all_addresses(request):
    form = AddressForm()
    all_address = ShippingAddress.objects.filter(user=request.user)
    
     # Check if any address has status=True
    has_default_address = any(all_address.status for all_address in all_address)

    # If no default address, set the status of the first address to True
    if not has_default_address and all_address:
        all_address[0].status = True
        all_address[0].save()
        
    context = {
        'address' : all_address,
        'form':form,
    }
    return render(request, 'user_profile/all-addresses.html', context)   
 
 
 
def add_address(request):
    form = AddressForm()  # Instantiate the form
    if request.method == 'POST':
        form = AddressForm(request.POST)
        if form.is_valid():
            print("Form is valid")
            # Save the address and set the user
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



def edit_address(request, address_id):
    # Retrieve the address from the database based on address_id
    address = get_object_or_404(ShippingAddress, id=address_id)

    # You should have a form to display the address details
    # Replace 'YourForm' with the actual form you are using
    form = AddressForm(instance=address)

    context = {
        'form': form,
        'address_id': address_id,
    }

    return render(request, 'user_profile/edit-address.html', context)


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


def delete_address(request, address_id):
    # Retrieve the address from the database based on address_id
    address_del = get_object_or_404(ShippingAddress, id=address_id)

    # Check if it's a POST request (form submission)
    if request.method == 'POST':
        # Delete the address
        address_del.delete()
        return redirect('user_profile:all_addresses')


    return render(request, 'user_profile/all-addresses.html')



def my_orders(request):
    # Retrieve orders for the logged-in user
    orders = Order.objects.filter(customer=request.user, complete=True).prefetch_related('orderitem_set__product')

     # Calculate the expected delivery date for each order
    for order in orders:
        order.expected_delivery_date = order.date_ordered + timedelta(days=3)
        order.seven_days_after_delivery = order.expected_delivery_date + timedelta(days=7)

        
    context = {
        'orders':orders,
    }
    return render(request, 'user_profile/my-orders.html', context)


def cancel_order(request, order_item_id):
    order_item = get_object_or_404(OrderItem, id=order_item_id)
    
    order_item.variation.stock += order_item.quantity
    order_item.variation.save() 
    
    
    order_item.delivery_status = 'CN'
    order_item.save()
    
     # If payment method is Razorpay, refund amount to user's wallet
    if order_item.order.payment_method == 'RAZ' or order_item.order.payment_method == 'WAL':
        user_wallet = Wallet.objects.get(user=request.user)
        total_amount = order_item.get_total() if callable(order_item.get_total) else order_item.get_total  
        user_wallet.balance += total_amount
        user_wallet.save()
    

    messages.success(request, 'Order canceled successfully.')

    return redirect('user_profile:my_orders')

def return_order(request, order_item_id):
    order_item = get_object_or_404(OrderItem, id=order_item_id)
    
    
    try:
        # Check if the order is eligible for return (you can implement your logic here)

        # Process the return
        order_item.delivery_status = 'RT'
        order_item.save()
        
         # Increase stock quantity
        order_item.variation.stock += order_item.quantity
        order_item.variation.save() 
        
        user_wallet = Wallet.objects.get(user=request.user)
        # Check if get_total is a method or an attribute
        total_amount = order_item.get_total() if callable(order_item.get_total) else order_item.get_total  
        user_wallet.balance += total_amount
        user_wallet.save()

        messages.success(request, 'Return Item request success.')
    except Exception as e:
        # Handle exceptions, log errors, or display an error message to the user
        messages.error(request, f'Error processing return request: {e}')
    
    return redirect('user_profile:my_orders')



def wallet(request):
    user_wallet = None

    if request.user.is_authenticated:
        user_wallet = Wallet.objects.get(user=request.user)

    context = {
        'user_wallet': user_wallet,
    }

    return render(request, 'user_profile/wallet.html', context)

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
                

    context = {
        'eligible_coupons': eligible_coupons,
        'used_coupons': used_coupons,
        'expired_coupons': expired_coupons,

    }

    return render(request, 'user_profile/coupon.html', context)

def wishlist(request):
    wishlist = Wishlist.objects.get(user=request.user)
    context = {
        'wishlist':wishlist,
    }
    return render(request, 'user_profile/wishlist.html',context)

def remove_item_wishlist(request, item_id):
    wishlist = get_object_or_404(Wishlist, user=request.user)
    product = get_object_or_404(Product, id=item_id)

    wishlist.items.remove(product)
    wishlist.save()
    
    return redirect('user_profile:wishlist')

from django.http import JsonResponse

def add_to_wishlist(request, product_id):
    response_data = {}

    try:
        if not request.user.is_authenticated:
            raise Exception('User not authenticated')

        wishlist, created = Wishlist.objects.get_or_create(user=request.user)
        product = get_object_or_404(Product, id=product_id)

        wishlist.items.add(product)
        wishlist.save()

        response_data['success'] = True
        response_data['message'] = 'Item added to your wishlist'
    except Exception as e:
        response_data['success'] = False
        response_data['error'] = str(e)

    return JsonResponse(response_data, safe=False)
