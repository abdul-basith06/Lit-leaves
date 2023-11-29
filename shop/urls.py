from django.urls import include, path
from . import views


app_name = 'shop'

urlpatterns = [
    path('store/', views.store, name="store"),    
    path('store/<slug:category_slug>/', views.store, name="store_by_category"),

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
    
    path('proceed_to_pay/', views.proceed_to_pay, name="proceed_to_pay"),
    path('place_order_razorpay/', views.place_order_razorpay, name='place_order_razorpay'),
    
    path('apply_coupon/<int:order_id>/', views.apply_coupon, name='apply_coupon'),
    path('remove_coupon/<int:order_id>/', views.remove_coupon, name='remove_coupon'),


    # path('remove_coupon/', views.remove_coupon, name='remove_coupon'),



]
