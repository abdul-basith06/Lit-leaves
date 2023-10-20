from django.urls import include, path
from . import views

app_name = 'admin_panel'

urlpatterns = [
    path('dash/', views.admin_dash, name='admin_dash'),
    path('user_management/', views.user_management, name='user_management'),
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



   

 ]
