from django.contrib import admin
from django.urls import path,include
from . import views


urlpatterns = [
    path('home/',views.store,name="store"),
    #path('cart/',views.cart,name="cart"),
    #path('checkout/',views.checkout,name="checkout"),
    path('category/<int:categories_id>/',views.product,name="product"),
    path('search/',views.search,name="search"),
    path('cart/',views.cart,name="cart"),
    path('displayCart/',views.displayCart,name="displayCart"),
    path('remove/',views.remove,name="remove"),
    path('plus/',views.plus,name="plus"),
    path('minus/',views.minus,name="minus"),
    path('complete/',views.complete,name="complete"),
    path('history/',views.displayHistory,name="history"),
    path('clear/',views.clearCart,name="clear")

]
