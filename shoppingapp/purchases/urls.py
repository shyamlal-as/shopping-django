from django.urls import path
from .views import add_to_cart
from .views import cart

urlpatterns = [
    path('',cart,name='cart'),
    path('add/<slug>',add_to_cart,name='addTocart'),
]