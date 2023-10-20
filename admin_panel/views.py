from django.shortcuts import render,redirect
from .models import *
from userauths.models import User
from django.contrib import messages
# from .forms import CategoryEditForm
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from .models import Categories



# Create your views here.
from django.shortcuts import render, redirect
from .models import Categories



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

def category(request):
    cat = Categories.objects.all()
    context = {
        'cat': cat
    }
    return render(request, 'admin_panel/category.html',context)

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

# def update_category(request, category_id):
#     category = Categories.objects.get(pk=category_id)
    
#     if request.method == 'POST':
#         category.name = request.POST['category_name']
#         category.save()
#         return redirect('admin_panel:category')  # Redirect to the category listing page

#     # If it's not a POST request, show the edit modal again.
#     context = {
#         'category': category,
#     }
    
#     return render(request, 'edit_category_modal.html', context)


# def edit_category(request, category_id):
#     category = Categories.objects.get(pk=category_id)

#     if request.method == 'POST':
#         form = CategoryEditForm(request.POST)
#         if form.is_valid():
#             category.name = form.cleaned_data['category_name']
#             category.save()
#             # Redirect or add a success message
#             return redirect('admin_panel:category')
#     else:
#         form = CategoryEditForm(initial={'category_name': category.name})

#     return render(request, 'admin_panel/category.html', {'form': form, 'category': category})

 
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