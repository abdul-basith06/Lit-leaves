from django.urls import include, path
from . import views


app_name = 'shop'

urlpatterns = [
    path('store/', views.store, name="store"),
    path('product/<int:product_id>/', views.product, name="product"),
    path('get_variation_stock/<int:variation_id>/', views.get_variation_stock, name='get_variation_stock'),
    path('cart/', views.cart, name="cart"),
    
    path('updateitem/', views.updateItem, name="updateitem"),
    path('clearitem/', views.clearItem, name="clearitem"),
    
    path('checkout/', views.checkout, name="checkout"),
    path('change_address/<int:address_id>/', views.change_address, name='change_address'),
    path('addaddress/', views.addaddress, name="addaddress"),
    path('update_address/', views.update_address, name="update_address"),  
    path('place_order/', views.place_order, name='place_order'),
    path('orderplaced/', views.order_placed_view, name='orderplaced'),


]
