from django.urls import path, re_path, include
from django.conf.urls import url

app_name = 'api'


urlpatterns = [

    #Version 1

    path('v1/',include('purchases.api.v1.urls', 'purchase_api_v1')),


    ]