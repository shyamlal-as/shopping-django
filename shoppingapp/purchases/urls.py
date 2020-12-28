from django.urls import path,include
from . import views


urlpatterns = [

    path('',views.cart,name="cart"),
    path('clear/',views.clearCart,name="clear"),
    path('displayCart/',views.displayCart,name="displayCart"),
    path('remove/',views.remove,name="remove"),
    path('plus/',views.plus,name="plus"),
    path('minus/',views.minus,name="minus"),
    path('complete/',views.complete,name="complete"),

]