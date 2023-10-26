from django.shortcuts import render,redirect
from .models import *
from userauths.models import User
from django.contrib import messages
from django.shortcuts import get_object_or_404
# from .forms import CategoryEditForm
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from .models import *

# def product_details(request):
#     return render(request, 'shop/product.html')
    

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
        stock = request.POST.get('stock')
        
        # Update the product details
        product.name = name
        product.description = description
        product.price = price
        product.category_id = category_id
        product.stock = stock
        
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
        stock = request.POST.get('stock')

        category = Categories.objects.get(pk=category_id)

        product = Product.objects.create(
            name=name,
            description=description,
            author=author,
            price=price,
            category=category,
            stock=stock
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
    all_cat = Categories.objects.all() 
    context = {
        'all_cat' : all_cat
    } 
    return render(request, 'admin_panel/add_products.html',context)


def products(request):
    pro1 = Product.objects.all()
    
    context = {
        'pro1': pro1,
    }
    return render(request, 'admin_panel/products.html',context)

def category(request):
    cat1 = Categories.objects.all()
    context = {
        'cat1': cat1
    }
    return render(request, 'admin_panel/category.html',context)



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
    return redirect('admin_panel:category')

def unblock_category(request, category_id):
    category = Categories.objects.get(pk=category_id)
    category.is_active = True
    category.save()
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


 
def delete_category(request, category_id):
    if request.method == 'POST':
        try:
            category = Categories.objects.get(pk=category_id)
            category.delete()
            messages.success(request, 'Category deleted successfully.')
        except Categories.DoesNotExist:
            messages.error(request, 'Category not found.')
    else:
        messages.error(request, 'Invalid request method')  # Add this line for debugging

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

def admin_dash(request):
    return render(request, 'admin_panel/admin_dash.html')

def user_management(request):
    cus = User.objects.all()
    context = {
        'cus' : cus,
    }
    return render(request, 'admin_panel/user_manage.html',context)