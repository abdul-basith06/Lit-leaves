from django.shortcuts import render
from django.utils import timezone
from django.db.models import Sum
from admin_panel.models import *
from shop.models import *
from django.http import HttpResponse, JsonResponse  

def index(request):
    user = request.user
    products = Product.objects.all()
    current_time = timezone.now()
    
    recent_products = Product.objects.filter(date_added__gte=current_time - timezone.timedelta(days=100))[:6]
    
    most_sold_products = Product.objects.filter(
        orderitem__delivery_status='D'  # 'D' represents Delivered status
    ).annotate(
        total_quantity_sold=Sum('orderitem__quantity')
    ).order_by('-total_quantity_sold')[:10]
    
    categories = Categories.objects.filter(is_active=True)
    
    if user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        cartItems = order.get_cart_items
    else:
        order = None
        cartItems = 0    
    
    context = {
        "products" : most_sold_products,
        'categories':categories,
        "recent_products": recent_products,
        'cartItems':cartItems,
    }
    return render(request, 'home/index.html',context)

def search_suggestions(request):
    term = request.GET.get('term', '')
    suggestions = Product.objects.filter(name__icontains=term)[:5] 
    data = [{'label': product.name, 'value': product.name, 'url': reverse('shop:product', args=[product.id])} for product in suggestions]
    return JsonResponse(data, safe=False)