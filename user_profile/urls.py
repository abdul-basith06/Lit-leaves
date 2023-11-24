from django.urls import include, path
from . import views

app_name = 'user_profile'


urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),
    path('editprofile/', views.editprofile, name='editprofile'),
    path('update_avatar/', views.update_avatar, name='update_avatar'),
    path('editpassword/', views.editpassword, name='editpassword'),
    
    path('all_addresses/', views.all_addresses, name='all_addresses'),
    path('add_address/', views.add_address, name='add_address'),
    path('edit_address/<int:address_id>/', views.edit_address, name='edit_address'),
    path('update_address/<int:address_id>/', views.update_address, name='update_address'),
    path('delete_address/<int:address_id>/', views.delete_address, name='delete_address'),

    path('my_orders/', views.my_orders, name='my_orders'),
    path('cancel_order/<int:order_item_id>/', views.cancel_order, name='cancel_order'),
    path('return_order/<int:order_item_id>/', views.return_order, name='return_order'),

    
    path('wallet/', views.wallet, name='wallet'),
    path('coupons/', views.coupons, name='coupons'),
    path('wishlist/', views.wishlist, name='wishlist'),
    path('remove_item_wishlist/<int:item_id>/', views.remove_item_wishlist, name='remove_item_wishlist'),
    path('add_to_wishlist/<int:product_id>/', views.add_to_wishlist, name='add_to_wishlist'),







 ]
