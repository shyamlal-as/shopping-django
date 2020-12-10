from django.urls import path, re_path
from django.conf.urls import url
from store.api.views import api_detail_product_viewv1,api_detail_product_viewv2,api_category_view

app_name = 'store'


urlpatterns = [
    #Product Versions
    path('v1/product/<slug>/',api_detail_product_viewv1,name = "details"),
    path('v2/product/<slug>/',api_detail_product_viewv2,name = "details"),
    
    #Categories
    path('categories/<slug>/',api_category_view,name='category_view'),
]
