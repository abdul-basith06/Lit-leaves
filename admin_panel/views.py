from django.http import Http404, JsonResponse
from django.shortcuts import render,redirect
from datetime import datetime, timedelta
from .forms import CouponForm
from .models import *
from django.db.models import Sum, F, DecimalField
from userauths.models import User
from collections import defaultdict
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.views.decorators.cache import never_cache
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.shortcuts import get_object_or_404
# from .forms import CategoryEditForm
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from shop.models import *


from django.contrib.auth.decorators import user_passes_test

def superuser_required(view_func):
    """
    Decorator for views that checks that the user is a superuser.
    """
    actual_decorator = user_passes_test(
        lambda u: u.is_active and u.is_superuser,
        login_url='admin_panel:admin_login',
    )
    return actual_decorator(view_func)

def admin_login(request):
    if request.user.is_authenticated and request.user.username == 'basi':
        return redirect('admin_panel:admin_dash')
    if request.method == 'POST':
        admin_name = request.POST['username']
        password = request.POST['password']
        if admin_name == 'basi' and password == '12369':
            user = authenticate(request, username=admin_name, password=password)

            if user is not None:
                login(request, user)
                return redirect('admin_panel:admin_dash')
        else:
            # Authentication failed, show an error message
            messages.error(request, 'Invalid username or password.')

    return render(request, 'admin_panel/admin_login.html')
    
@never_cache
@superuser_required
def admin_logout(request):
    if request.user.is_authenticated:
        request.session.flush()
    return redirect('admin_panel:admin_login')
       
@superuser_required
def unlist_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    product.is_active = False  # Set the product as inactive
    product.save()
    return redirect('admin_panel:products')

@superuser_required
def list_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    product.is_active = True  # Set the product as active
    product.save()
    return redirect('admin_panel:products')


@superuser_required
def update_products(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    if request.method == 'POST':
        # Get the updated data from the form
        name = request.POST.get('name')
        description = request.POST.get('description')
        price = request.POST.get('price')
        category_id = request.POST.get('category')
        
        # Update the product details
        product.name = name
        product.description = description
        product.price = price
        product.category_id = category_id
        
         # Handle image updates
        new_images = request.FILES.getlist('new_images')
        delete_images = request.POST.getlist('delete_images')

        # Handle adding new images (you need to adapt this logic based on your model)
        for new_image in new_images:
            product_image = ProductImage(image=new_image, product=product)
            product_image.save()

        # Handle image deletions
        for image_id in delete_images:
            product_image = ProductImage.objects.get(id=image_id)
            product_image.delete()
            
        # Save the updated product
        product.save()

        # Redirect to the product listing page
        return redirect('admin_panel:products')

    context = {
        'product': product,
    }

    return render(request, 'admin_panel/edit_product.html', context)

@superuser_required
def edit_products(request, product_id):
    product = Product.objects.get(pk=product_id)
    cat2 = Categories.objects.all()
    context = {
        'product': product,
        'cat2': cat2,
    }
    return render(request, 'admin_panel/edit_products.html',context)

@superuser_required
def addd_products(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')
        author = request.POST.get('author')
        price = request.POST.get('price')
        category_id = request.POST.get('category')
        
        if int(price) <= 0:
            messages.error(request, "Enter a valid price !")
            return redirect('admin_panel:add_products')
      
       
        category = Categories.objects.get(pk=category_id)

        product = Product.objects.create(
            name=name,
            description=description,
            author=author,
            price=price,
            category=category,
        )

        images = request.FILES.getlist('image')  # Get a list of uploaded images

        for image in images:
            ProductImage.objects.create(product=product, image=image)

        return redirect('admin_panel:products')
    else:
        # Handle the case where the request method is not POST (e.g., GET)
        # You may want to render a form or redirect to the add_products page with an error message.
        pass

    
@superuser_required    
def add_products(request):
    all_cat = Categories.objects.filter(is_active=True)
    context = {
        'all_cat' : all_cat
    } 
    return render(request, 'admin_panel/add_products.html',context)

@superuser_required
def product_variation(request, product_id):
    product = Product.objects.get(pk=product_id)
    languages = Language.objects.all()  # Query all languages
    context = {
        'product': product,
        'languages' : languages,
    }
    
    return render(request, 'admin_panel/product_variation.html', context)

@superuser_required
def edit_stock_variation(request, variation_id):
    try:
        product_variation = ProductLanguageVariation.objects.get(pk=variation_id)
    except ProductLanguageVariation.DoesNotExist:
        raise Http404("Product Variation does not exist")

    if request.method == 'POST':
        # Update the stock and language fields
        product_variation.stock = request.POST['stock']
        product_variation.language_id = request.POST['language']
        product_variation.save()
        return redirect('admin_panel:product_variation', product_id=product_variation.product.id)  # Redirect to the product variations page

    context = {
        'product_variation': product_variation,
    }

    return render(request, 'admin_panel/product_variation.html', context)


@superuser_required
def add_variant(request, product_id):
    if request.method == 'POST':
        product = Product.objects.get(pk=product_id)
        language_id = request.POST['language']
        stock = request.POST['stock']
        ProductLanguageVariation.objects.create(product=product, language_id=language_id, stock=stock)
        return redirect('admin_panel:product_variation', product_id=product_id)

    return render(request, 'admin_panel/product_variation.html')  



@superuser_required
def products(request):
    search_query = request.GET.get('key')  # Get the search query from the URL parameters
    pro1 = Product.objects.all()

    if search_query:
        pro1 = pro1.filter(Q(name__icontains=search_query))
        
        
     # Fetch ProductLanguageVariation data for each product
    # for product in pro1:
    #     product.variations = product.productlanguagevariation_set.all()    

    context = {
        'pro1': pro1,
       'search_query': search_query,
        
    }
    return render(request, 'admin_panel/products.html', context)



@superuser_required
def category(request):
    search_query = request.GET.get('key')  # Get the search query from the request
    cat1 = Categories.objects.all()

    if search_query:
        # If there's a search query, filter categories based on name
        cat1 = cat1.filter(name__icontains=search_query)
     
    context = {
        'cat1': cat1,
        'search_query': search_query,  # Pass the search query back to the template
    }
    return render(request, 'admin_panel/category.html', context)



@superuser_required
def add_category(request):
    if request.method == 'POST':
        # Get the category name from the POST data
        category_name = request.POST.get('category_name')

        # Get the uploaded icon file
        icon_file = request.FILES.get('category_icon')

        # Check if the category name is not empty and an icon file is provided
        if category_name and icon_file:
            # Create a new category instance
            category = Categories(name=category_name)

            # Handle the uploaded icon file
            icon_path = default_storage.save('images/category_icons/' + icon_file.name, ContentFile(icon_file.read()))
            category.icon = icon_path

            category.save()

            # Redirect to the category listing page
            return redirect('admin_panel:category')

    return render(request, 'add_category_modal.html')

@superuser_required
def block_category(request, category_id):
    category = Categories.objects.get(pk=category_id)
    category.is_active = False
    category.save()
    Product.objects.filter(category=category).update(is_active=False)
    return redirect('admin_panel:category')

@superuser_required
def unblock_category(request, category_id):
    category = Categories.objects.get(pk=category_id)
    category.is_active = True
    category.save()
    Product.objects.filter(category=category).update(is_active=True)
    return redirect('admin_panel:category')

@superuser_required
def edit_category(request, category_id):
    category = Categories.objects.get(pk=category_id)
    
    context = {
        'category': category,
    }
    
    return render(request, 'edit_category_modal.html', context)

@superuser_required
def update_category(request, category_id):
    category = Categories.objects.get(pk=category_id)
    
    if request.method == 'POST':
        category.name = request.POST['category_name']
        if 'category_icon' in request.FILES:
            icon_file = request.FILES['category_icon']
            icon_path = default_storage.save('images/category_icons/' + icon_file.name, ContentFile(icon_file.read()))
            category.icon = icon_path
        category.save()
        return redirect('admin_panel:category')  # Redirect to the category listing page

    # If it's not a POST request, show the edit modal again.
    context = {
        'category': category,
    }
    
    return render(request, 'edit_category_modal.html', context)



@superuser_required
def delete_category(request, category_id):
    if request.method == 'POST':
        category = get_object_or_404(Categories, pk=category_id)

        # Update is_active for products in this category
        Product.objects.filter(category=category).update(is_active=False)

        category.delete()
        messages.success(request, 'Category and associated products deactivated successfully.')
    else:
        messages.error(request, 'Invalid request method')

    return redirect('admin_panel:category')
 
@superuser_required
def block_user(request, user_id):
    user = User.objects.get(pk=user_id)
    user.is_active = False
    user.save()
    return redirect('admin_panel:user_management')

@superuser_required
def unblock_user(request, user_id):
    user = User.objects.get(pk=user_id)
    user.is_active = True
    user.save()
    return redirect('admin_panel:user_management')



@superuser_required
def user_management(request):
    search_query = request.GET.get('key')
    cus = User.objects.all()
    
    if search_query:
        cus = cus.filter(Q(username__icontains=search_query) | Q(email__icontains=search_query))

    context = {
        'cus': cus,
        'search_query': search_query,
    }
    return render(request, 'admin_panel/user_manage.html', context)


@superuser_required
def admin_dash(request):
    all_orders = Order.objects.all()
    all_variations = ProductLanguageVariation.objects.all()
    all_order_items = OrderItem.objects.all()
    
     # Get the filter type from the request
    filter_type = request.GET.get('filter_type', 'all')  # Default to 'all' if not specified

    # Calculate start date based on the filter type
    if filter_type == 'day':
        start_date = datetime.now() - timedelta(days=1)
    elif filter_type == 'week':
        start_date = datetime.now() - timedelta(weeks=1)
    elif filter_type == 'month':
        start_date = datetime.now() - timedelta(weeks=4)  # Approximating a month as 4 weeks
    elif filter_type == 'year':
        start_date = datetime.now() - timedelta(weeks=52)  # Approximating a year as 52 weeks
    else:
        start_date = None  # No filter, get all orders

    # Apply date filter if start_date is available
    if start_date:
        all_orders = all_orders.filter(date_ordered__gte=start_date)

    # Calculate total revenue
    total_revenue = sum(order.get_cart_total for order in all_orders)
    total_sales = sum(order.get_cart_items for order in all_orders)
    total_stock = sum(variation.stock for variation in all_variations)
    
     # Fetch payment history
    cod_orders = Order.objects.filter(payment_method='COD')
    online_orders = Order.objects.filter(payment_method='RAZ')  # Assuming 'RAZ' is for online payments
    wallet_orders = Order.objects.filter(payment_method='WAL')

    cod_count = cod_orders.count()
    online_count = online_orders.count()
    wallet_count = wallet_orders.count()

    cod_total = sum(order.get_cart_total for order in cod_orders)
    online_total = sum(order.get_cart_total for order in online_orders)
    wallet_total = sum(order.get_cart_total for order in wallet_orders)

    
    context = {
        'total_revenue': total_revenue,
        'total_sales' : total_sales,
        'total_stock':total_stock,
        'all_orders':all_orders,
        'all_order_items':all_order_items,
        'cod_count': cod_count,
        'online_count': online_count,
        'wallet_count': wallet_count,
        'cod_total': cod_total,
        'online_total': online_total,
        'wallet_total': wallet_total,
        'filter_type': filter_type,  

    }
    return render(request, 'admin_panel/admin_dash.html', context)

@superuser_required
def order_management(request):
    order = Order.objects.all()
    context = {
        'order' : order,
    }
    return render(request, 'admin_panel/orders.html', context)

@superuser_required
def manage_order(request, order_id, orderitem_id):
    order = get_object_or_404(Order, id=order_id)
    order_item = get_object_or_404(OrderItem, id=orderitem_id)


    context = {
        'order': order,
        'order_item': order_item,
    }

    return render(request, 'admin_panel/manage_order.html', context)

@superuser_required
def cancel_order(request, order_item_id):
    order_item = get_object_or_404(OrderItem, id=order_item_id)
    
     # Increase stock quantity
    order_item.variation.stock += order_item.quantity
    order_item.variation.save() 
    
    # Update delivery status to 'CN' (Cancelled)
    order_item.delivery_status = 'CN'
    order_item.save()
    
    if order_item.order.payment_method in ['WAL', 'RAZ']:  # Assuming 'RAZ' is for Razorpay
        # Refund the amount
        refund_amount = order_item.get_total() if callable(order_item.get_total) else order_item.get_total
        print('refund_amount')

        # Get the user and order
        user = order_item.order.customer
        user_wallet = Wallet.objects.get(user=user)
        order = order_item.order

        # Perform the refund to the wallet or original payment method
        if order.payment_method == 'WAL' or order.payment_method == 'RAZ':
            # Update user's wallet balance
            user_wallet.balance += refund_amount
            user_wallet.save()

    messages.success(request, 'Order canceled successfully.')

    return redirect('admin_panel:order_management')

@superuser_required
def update_order_status(request, order_item_id):
    if request.method == 'POST':
        delivery_status = request.POST.get('delivery_status')
       
        order_item = OrderItem.objects.get(id=order_item_id)

        order_item.delivery_status = delivery_status
        order_item.save()

        return redirect('admin_panel:order_management')  

    return render(request, 'admin_panel/order_management.html')

@superuser_required
def coupons(request):
    coupon = Coupon.objects.all()
    context = {
        'coupon':coupon,
    }
    return render(request, 'admin_panel/coupons.html',context)

@superuser_required
def add_coupons(request):
    form = CouponForm()

    if request.method == 'POST':
        form = CouponForm(request.POST)
        if form.is_valid():
            coupon = form.save()
            messages.success(request, 'Coupon added successfully.')
            return redirect('admin_panel:coupons')
        else:
            messages.error(request, 'Error adding the coupon. Please check the form data.')
    context = {
        'form':form,
    }        
    return render(request, 'admin_panel/add_coupons.html',context)

@superuser_required
def edit_coupon(request, coupon_id):
    coupon = get_object_or_404(Coupon, id=coupon_id)
    form = CouponForm(instance=coupon)
    context = {
        'form':form,
        'coupon_id':coupon_id,
    }
    return render(request, 'admin_panel/edit_coupon.html',context)

@superuser_required
def update_coupon(request, coupon_id):
    coupon = get_object_or_404(Coupon, id=coupon_id)
    if request.method == 'POST':
        form = CouponForm(request.POST, instance=coupon)
        if form.is_valid():
            form.save()
            messages.success(request, 'Coupon edited successfully.')
            return redirect('admin_panel:coupons')
    else:
        form = CouponForm(instance=coupon)
    context = {
        'form':form,
        'coupon_id':coupon_id,
    }
    return render(request, 'admin_panel/edit_coupon.html',context)

@superuser_required
def delete_coupon(request, coupon_id):
    coupon = get_object_or_404(Coupon, id=coupon_id)
    if request.method == 'POST':
        coupon.delete()
        messages.success(request, 'Coupon deleted successfully.')
        return redirect('admin_panel:coupons')
    
    return render(request, 'admin_panel/coupons.html')
    
@superuser_required    
def sales_report(request):
    all_orders = Order.objects.all()
    all_variations = ProductLanguageVariation.objects.all()
    all_order_items = OrderItem.objects.all()
    
    total_sales = sum(order.get_cart_items for order in all_orders)
    
    context = {
        'total_sales':total_sales,
    }

    return render(request, 'admin_panel/sales_report.html',context)    

@superuser_required
def sales_portfolio(request):
    print("coming into this view>>>>>>>>>>>>>>>>>>>>>")
    time_period = request.POST.get('date', 'week') 

    end_date = timezone.now()

    if time_period == 'week':
        # Calculate start_date for the last 8 weeks (including the current week)
        start_date = end_date - timedelta(weeks=8)
    elif time_period == 'month':
        # Calculate start_date for the last 12 months
        start_date = end_date - timedelta(days=365)
    elif time_period == 'year':
        # Calculate start_date for the last 10 years
        start_date = end_date - timedelta(days=3650)
    else:
        # Default to 'week' if an invalid time period is provided
        start_date = end_date - timedelta(weeks=8)

    # Fetch orders within the selected time period
    orders_within_period = Order.objects.filter(date_ordered__range=[start_date, end_date])

    # Group orders by date
    sales_data = orders_within_period.values('date_ordered')

    # Calculate total sales for each date
    sales_data = sales_data.annotate(
        total_sales=Sum(F('orderitem__product__price') * F('orderitem__quantity'), output_field=DecimalField())
    )

    # Extract labels (dates) and data (total sales)
    labels = [order['date_ordered'].strftime('%Y-%m-%d') for order in sales_data]
    data = [order['total_sales'] if order['total_sales'] is not None else 0 for order in sales_data]

    # Calculate overall total sales
    overall_total_sales = sum(data)
    
    print('Labels:', labels)
    print('Data:', data)
    print('Overall Total Sales:', overall_total_sales)

    return JsonResponse({'labels': labels, 'data': data, 'overall_total_sales': overall_total_sales})






















# def sales_portfolio(request):
#     print("coming into this view>>>>>>>>>>>>>>>>>>>>>")
#     time_period = request.POST.get('date', 'week') 

#     end_date = timezone.now()
#     if time_period == 'week':
#         start_date = end_date - timezone.timedelta(days=7)
#     elif time_period == 'month':
#         start_date = end_date - timezone.timedelta(days=30)
#     elif time_period == 'year':
#         start_date = end_date - timezone.timedelta(days=365)
#     else:
#         # Default to 'week' if an invalid time period is provided
#         start_date = end_date - timezone.timedelta(days=7)

#     # Fetch orders within the selected time period
#     orders_within_period = Order.objects.filter(date_ordered__range=[start_date, end_date])

#     # Group orders by date
#     sales_data = orders_within_period.values('date_ordered')

#     # Calculate total sales for each date
#     sales_data = sales_data.annotate(
#         total_sales=Sum(F('orderitem__product__price') * F('orderitem__quantity'), output_field=DecimalField())
#     )

#     # Extract labels (dates) and data (total sales)
#     labels = [order['date_ordered'].strftime('%Y-%m-%d') for order in sales_data]
#     data = [order['total_sales'] if order['total_sales'] is not None else 0 for order in sales_data]

#     # Calculate overall total sales
#     overall_total_sales = sum(data)
    
#     print('Labels:', labels)
#     print('Data:', data)
#     print('Overall Total Sales:', overall_total_sales)

#     return JsonResponse({'labels': labels, 'data': data, 'overall_total_sales': overall_total_sales})



    