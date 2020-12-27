from django.urls import path, re_path, include
from django.conf.urls import url

app_name = 'api'


urlpatterns = [

    #Version 1

    path('v1/',include('store.api.v1.urls', 'product_api_v1')),


    ]