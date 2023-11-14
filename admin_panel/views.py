from django.http import Http404
from django.shortcuts import render,redirect
from .models import *
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
def admin_logout(request):
    if request.user.is_authenticated:
        request.session.flush()
    return redirect('admin_panel:admin_login')
       

def unlist_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    product.is_active = False  # Set the product as inactive
    product.save()
    return redirect('admin_panel:products')

def list_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    product.is_active = True  # Set the product as active
    product.save()
    return redirect('admin_panel:products')


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

def edit_products(request, product_id):
    product = Product.objects.get(pk=product_id)
    cat2 = Categories.objects.all()
    context = {
        'product': product,
        'cat2': cat2,
    }
    return render(request, 'admin_panel/edit_products.html',context)

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

    
def add_products(request):
    all_cat = Categories.objects.filter(is_active=True)
    context = {
        'all_cat' : all_cat
    } 
    return render(request, 'admin_panel/add_products.html',context)

@login_required(login_url='admin_panel:admin_login')
def product_variation(request, product_id):
    product = Product.objects.get(pk=product_id)
    languages = Language.objects.all()  # Query all languages
    context = {
        'product': product,
        'languages' : languages,
    }
    
    return render(request, 'admin_panel/product_variation.html', context)

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


def add_variant(request, product_id):
    if request.method == 'POST':
        product = Product.objects.get(pk=product_id)
        language_id = request.POST['language']
        stock = request.POST['stock']
        ProductLanguageVariation.objects.create(product=product, language_id=language_id, stock=stock)
        return redirect('admin_panel:product_variation', product_id=product_id)

    return render(request, 'admin_panel/product_variation.html')  



@login_required(login_url='admin_panel:admin_login')
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



@login_required(login_url='admin_panel:admin_login')
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


def block_category(request, category_id):
    category = Categories.objects.get(pk=category_id)
    category.is_active = False
    category.save()
    Product.objects.filter(category=category).update(is_active=False)
    return redirect('admin_panel:category')

def unblock_category(request, category_id):
    category = Categories.objects.get(pk=category_id)
    category.is_active = True
    category.save()
    Product.objects.filter(category=category).update(is_active=True)
    return redirect('admin_panel:category')


def edit_category(request, category_id):
    category = Categories.objects.get(pk=category_id)
    
    context = {
        'category': category,
    }
    
    return render(request, 'edit_category_modal.html', context)

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



@login_required(login_url='admin_panel:admin_login')
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
 
    
def block_user(request, user_id):
    user = User.objects.get(pk=user_id)
    user.is_active = False
    user.save()
    return redirect('admin_panel:user_management')

def unblock_user(request, user_id):
    user = User.objects.get(pk=user_id)
    user.is_active = True
    user.save()
    return redirect('admin_panel:user_management')



@login_required(login_url='admin_panel:admin_login')
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


@login_required(login_url='admin_panel:admin_login')
def admin_dash(request):
    return render(request, 'admin_panel/admin_dash.html')

def order_management(request):
    order = Order.objects.all()
    context = {
        'order' : order,
    }
    return render(request, 'admin_panel/orders.html', context)


def manage_order(request, order_id, orderitem_id):
    # Retrieve the specific order and order item
    order = get_object_or_404(Order, id=order_id)
    order_item = get_object_or_404(OrderItem, id=orderitem_id)

    # Your existing logic for rendering the manage_order page

    context = {
        'order': order,
        'order_item': order_item,
    }

    return render(request, 'admin_panel/manage_order.html', context)