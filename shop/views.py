from django.shortcuts import render
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from admin_panel.models import *

from django.shortcuts import render, get_object_or_404


# Create your views here.


def store(request):
    products = Product.objects.all()  # Fetch all products
    paginator = Paginator(products, 9)  # Show 10 products per page

    page = request.GET.get('page')
    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        products = paginator.page(1)
    except EmptyPage:
        products = paginator.page(paginator.num_pages)

    return render(request, 'shop/store.html', {'products': products})



def product(request, product_id):
    selected_product = Product.objects.get(pk=product_id)
    category = selected_product.category

    # Query related products from the same category, excluding the selected product
    related_products = Product.objects.filter(category=category).exclude(pk=selected_product.id)[:4]

    context = {
        'product': selected_product,
        'related_products': related_products,
    }

    return render(request, 'shop/product.html', context)
