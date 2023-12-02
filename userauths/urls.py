from django.urls import include, path
from . import views

app_name = 'userauths'

urlpatterns = [
    path('sign-up/', views.user_register, name='sign-up'),
    path('otp_verification/', views.otp_verification, name='otp_verification'),
    # path('resend_otp/', views.resend_otp, name='resend_otp'),

    
    
    path('otp_verification2/', views.otp_verification2, name='otp_verification2'),
    path('sign-in/', views.user_sign, name='sign-in'),
    # path('verify/', views.user_verify, name='verify'),
    path('logout/', views.user_logout, name='logout'),


 ]
