from django.urls import path, re_path
from django.conf.urls import url
from . import views

app_name = 'apps'


urlpatterns = [
    #Product Versions
    path('product/<slug>/',views.api_detail_product_view,name = "details"),
    
    #Categories
    path('category/<slug>/',views.api_category_view,name = "details"),
]