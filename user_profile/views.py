from django.shortcuts import redirect, render
from admin_panel.models import *
from .forms import *
from shop.models import *
from .models import *
from django.http import HttpResponse  # Import HttpResponse from django.http

def dashboard(request):
    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()  # Correctly access order items
        cartItems = order.get_cart_items
    try:
        profile = UserProfile.objects.get(user=request.user)
    except UserProfile.DoesNotExist:
        profile = None   
    context = {
        'cartItems' : cartItems,
        'profile' : profile,
    }
    return render(request, 'user_profile/dashboard.html', context)


def update_avatar(request):
    if request.method == 'POST':
        user_profile = UserProfile.objects.get(user=request.user)
        user_profile.dp = request.FILES['image']  # 'image' should match the input name attribute in your form
        user_profile.save()
        return redirect('user_profile:dashboard')

    return render(request, 'user_profile/dashboard.html')


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