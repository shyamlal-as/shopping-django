from django.contrib import admin
from django.urls import path,include
from . import views
from users.views import user_view


urlpatterns = [
    path('',views.store,name="store"),
    #path('checkout/',views.checkout,name="checkout"),
    path('category/<int:category_id>/',views.product,name="product"),
    path('search/',views.search,name="search"),
    

    path('details/<slug>',views.details,name="product-detail"),
    path('profile',views.profile,name="profile"),
    path('edit-profile',user_view,name="edit-profile"),


    
]