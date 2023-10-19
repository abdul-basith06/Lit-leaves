from django.urls import include, path
from . import views

app_name = 'admin_panel'

urlpatterns = [
    path('dash/', views.admin_dash, name='admin_dash'),
    path('user_management/', views.user_management, name='user_management'),
    # path('user_management/block_unblock/<int:user_id>/', views.block_unblock_user, name='block_unblock_user'),
    path('block_user/<int:user_id>/', views.block_user, name='block_user'),
    path('unblock_user/<int:user_id>/', views.unblock_user, name='unblock_user'),
   
   


 ]
