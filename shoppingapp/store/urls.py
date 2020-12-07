from django.urls import path
from . import views


urlpatterns = [
    #path('', views.Home, name='store-home'),

    path('',views.store,name="store"),
    path('cart/',views.cart,name="cart"),
    path('checkout/',views.checkout,name="checkout"),
    path('category/<int:categories_id>/',views.product,name="product"),
    path('search/',views.search,name="search"),
    path('product/<slug>/', views.details,name='product-detail'),
]
