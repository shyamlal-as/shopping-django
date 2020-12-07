from django.urls import path
from store.api.views import api_detail_product_view

app_name = 'store'

urlpatterns = [
    path('product/<slug>/',api_detail_product_view,name = "details")
]