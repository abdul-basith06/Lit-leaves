from django.urls import include, path
from . import views

app_name = 'user_profile'


urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),
    path('editprofile/', views.editprofile, name='editprofile'),
    path('update_avatar/', views.update_avatar, name='update_avatar'),
    path('editpassword/', views.editpassword, name='editpassword'),
 ]
