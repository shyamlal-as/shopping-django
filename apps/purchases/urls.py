from django.urls import path,include
from .views import add_to_cart
from .views import cart

urlpatterns = [
    path('',cart,name='cart'),
    path('add/<slug>',add_to_cart,name='addTocart'),
    path('api/',include('purchases.api.urls'),name='apis'),
]