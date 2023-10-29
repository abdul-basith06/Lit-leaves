from django.urls import include, path
from . import views

app_name = 'admin_panel'

urlpatterns = [
    path('admin_login/', views.admin_login, name='admin_login'),
    path('admin_logout/', views.admin_logout, name='admin_logout'),
    path('dash/', views.admin_dash, name='admin_dash'),
    path('user_management/', views.user_management, name='user_management'), 
    # path('search_users/', views.search_users, name='search_users'),
    path('block_user/<int:user_id>/', views.block_user, name='block_user'),
    path('unblock_user/<int:user_id>/', views.unblock_user, name='unblock_user'),
    
    # category management urls begins
    path('category', views.category, name='category'),
    path('delete_category/<int:category_id>/', views.delete_category, name='delete_category'),
    path('edit_category/<int:category_id>/', views.edit_category, name='edit_category'),
    path('update_category/<int:category_id>/', views.update_category, name='update_category'),
    path('add_category/', views.add_category, name='add_category'),
    path('block_category/<int:category_id>/', views.block_category, name='block_category'),
    path('unblock_category/<int:category_id>/', views.unblock_category, name='unblock_category'),

    # Product management begins  
    path('products', views.products, name='products'),
    path('add_products', views.add_products, name='add_products'),
    path('addd_products', views.addd_products, name='addd_products'),
    path('edit_products/<int:product_id>/', views.edit_products, name='edit_products'),
    path('update_products/<int:product_id>/', views.update_products, name='update_products'),
    path('unlist_product/<int:product_id>/', views.unlist_product, name='unlist_product'),
    path('list_product/<int:product_id>/', views.list_product, name='list_product'),
    
    # path('product_details/', views.product_details, name='product_details'),
   

 ]
