from django.urls import include, path
from . import views


app_name = 'shop'

urlpatterns = [
    path('store/', views.store, name="store"),
    path('product/<int:product_id>/', views.product, name="product"),
    path('cart/', views.cart, name="cart"),
    
    path('updateitem/', views.updateItem, name="updateitem"),
    
    


]
