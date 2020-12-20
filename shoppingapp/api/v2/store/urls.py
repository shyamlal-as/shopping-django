from django.urls import path, re_path
from django.conf.urls import url
from api.v2.store.views import api_detail_product_view

app_name = 'api'


urlpatterns = [
    #Product Versions
    path('product/<slug>/',api_detail_product_view,name = "details"),
    
    #Categories
]
