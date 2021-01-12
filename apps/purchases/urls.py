from django.urls import path,include
from . import views

urlpatterns = [
    path('cart/',views.cart,name="cart"),
    path('displayCart/',views.displayCart,name="displayCart"),
    path('remove/',views.remove,name="remove"),
    path('plus/',views.plus,name="plus"),
    path('minus/',views.minus,name="minus"),
    path('complete/',views.complete,name="complete"),
    path('clear/',views.clearCart,name="clear"),
]