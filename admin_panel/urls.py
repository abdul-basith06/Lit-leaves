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
    path('add_language/', views.add_language, name='add_language'),
    path('block_category/<int:category_id>/', views.block_category, name='block_category'),
    path('unblock_category/<int:category_id>/', views.unblock_category, name='unblock_category'),

    # Product management begins  
    path('products', views.products, name='products'),
    
    path('product_variation/<int:product_id>/', views.product_variation, name='product_variation'), 
    path('edit_stock_variation/<int:variation_id>/', views.edit_stock_variation, name='edit_stock_variation'),
    path('add_variant/<int:product_id>/', views.add_variant, name='add_variant'), 
    
      
    path('add_products', views.add_products, name='add_products'),
    path('addd_products', views.addd_products, name='addd_products'),
    path('delete_product/<int:product_id>/', views.delete_product, name='delete_product'),
    path('edit_products/<int:product_id>/', views.edit_products, name='edit_products'),
    path('update_products/<int:product_id>/', views.update_products, name='update_products'),
    path('unlist_product/<int:product_id>/', views.unlist_product, name='unlist_product'),
    path('list_product/<int:product_id>/', views.list_product, name='list_product'),
    
    # path('product_details/', views.product_details, name='product_details'),
   
    path('order_management/', views.order_management, name='order_management'),
    path('manage_order/<int:order_id>/<int:orderitem_id>/', views.manage_order, name='manage_order'),
    path('cancel_order/<int:order_item_id>/', views.cancel_order, name='cancel_order'),
    path('update_order_status/<int:order_item_id>/', views.update_order_status, name='update_order_status'),
    
    path('coupons/', views.coupons, name='coupons'),
    path('add_coupons/', views.add_coupons, name='add_coupons'),
    path('edit_coupon/<int:coupon_id>/', views.edit_coupon, name='edit_coupon'),
    path('update_coupon/<int:coupon_id>/', views.update_coupon, name='update_coupon'),
    path('delete_coupon/<int:coupon_id>/', views.delete_coupon, name='delete_coupon'),


    path('sales_report/', views.sales_report, name='sales_report'),
    path('get_sales_data/<str:period>/', views.get_sales_data, name='get_sales_data'),
    
    path('sales_report_pdf/', views.sales_report_pdf, name='sales_report_pdf'),  # Add this line
    path('sales_report_excel/', views.sales_report_excel, name='sales_report_excel'),





    






 ]
