from django.contrib import admin
from django.urls import path,include
from . import views
from users.views import user_view


urlpatterns = [
    path('',views.store,name="store"),
    #path('cart/',views.cart,name="cart"),
    #path('checkout/',views.checkout,name="checkout"),
    path('category/<int:category_id>/',views.product,name="product"),
    path('search/',views.search,name="search"),
    path('seller/',views.seller,name="seller"),
    path('sellerAdd/',views.sellerAdd,name="sellerAdd"),
    path('upload/',views.upload,name="upload"),
    path('registerAsSeller/',views.registerAsSeller,name="sellerRegistration"),
    path('cart/',views.cart,name="cart"),

    #path('displayCart/',views.displayCart,name="displayCart"),
    path('displayCart/',views.testSearch,name="cart"),


    path('remove/',views.remove,name="remove"),
    path('plus/',views.plus,name="plus"),
    path('minus/',views.minus,name="minus"),
    path('complete/',views.complete,name="complete"),

    path('details/<slug>',views.details,name="product-detail"),
    path('profile',views.profile,name="profile"),
    path('edit-profile',user_view,name="edit-profile"),
    path('clear/',views.clearCart,name="clear"),
    #path('api/',include('store.api.urls'),name='apis'),

]