from django.urls import path
from . import views


urlpatterns = [
    #path('', views.Home, name='store-home'),

    path('',views.store,name="store"),
    path('cart/',views.cart,name="cart"),
    path('checkout/',views.checkout,name="checkout"),
    path('product/',views.product,name="product"),
]
