from django.urls import include, path
from . import views


app_name = 'shop'

urlpatterns = [
    path('store/', views.store, name="store"),
    # path('product/', views.product, name="product"),
    path('product/<int:product_id>/', views.product, name="product")

]
