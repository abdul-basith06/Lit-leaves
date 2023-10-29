from django.shortcuts import render
from admin_panel.models import *
from django.http import HttpResponse  # Import HttpResponse from django.http

def index(request):
    pro = Product.objects.all()
    context = {
        "products" : pro
    }
    return render(request, 'home/index.html',context)
