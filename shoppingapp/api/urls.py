from django.urls import path, re_path, include
from django.conf.urls import url

app_name = 'api'


urlpatterns = [

    #Version 1

    path('store/v1/',include('api.v1.store.urls', 'product_api_v1')),
    #path('users/v1/',include('api.v1.urls', 'users_api_v1')),
    path('cart/v1/',include('api.v1.purchases.urls','cart_api_v1')),

    #Version 2

    path('store/v2/',include('api.v2.store.urls', 'product_api_v2')),
    #path('users/v2/',include('api.v2.urls', 'users_api_v2')),
    path('cart/v2/',include('api.v2.purchases.urls','cart_api_v2')),

]
