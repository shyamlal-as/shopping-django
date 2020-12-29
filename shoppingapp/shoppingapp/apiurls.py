from django.urls import path,include


urlpatterns = [

    #Version 1

    path('v1/store/',include('store.api.v1.urls')),
    path('v1/cart/',include('purchases.api.v1.urls')),
    path('v1/users/',include('users.api.v1.urls')),

    #Version 2

    path('v2/store/',include('store.api.v2.urls')),
    path('v2/cart/',include('purchases.api.v2.urls')),

]