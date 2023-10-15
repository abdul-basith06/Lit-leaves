from django.shortcuts import render
from django.http import HttpResponse  # Import HttpResponse from django.http

def index(request):
    return render(request, 'home/index.html')
