from django.urls import include, path
from . import views

app_name = 'userauths'

urlpatterns = [
    path('sign-up/', views.user_register, name='sign-up'),
    path('otp_verification/', views.otp_verification, name='otp_verification'),
    path('resend_otp/', views.resend_otp, name='resend_otp'),
    path('resend_otp2/', views.resend_otp2, name='resend_otp2'),
    path('resend_otp3/', views.resend_otp3, name='resend_otp3'),


    
    
    path('otp_verification2/', views.otp_verification2, name='otp_verification2'),
    path('sign-in/', views.user_sign, name='sign-in'),
    
    path('forget_password/', views.forget_password, name='forget_password'),
    path('forgot_password/', views.forgot_password, name='forgot_password'),
    path('otp_verification_forget_password/', views.otp_verification_forget_password, name='otp_verification_forget_password'),
    path('set_password/', views.set_password, name='set_password'),
    # path('verify/', views.user_verify, name='verify'),
    path('logout/', views.user_logout, name='logout'),


 ]
