from django.urls import include, path
from . import views


app_name = 'home'

urlpatterns = [
    path('', views.index, name="index"),
    path('search_suggestions/', views.search_suggestions, name='search_suggestions'),
]
