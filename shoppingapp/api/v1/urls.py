from django.urls import path, re_path
from django.conf.urls import url
from api.v1.views import api_detail_product_view,api_category_view

app_name = 'api'


urlpatterns = [
    #Product Versions
    path('product/<slug>/',api_detail_product_view,name = "details"),
    
    #Categories
    path('categories/<slug>/',api_category_view,name='category_view'),
]
