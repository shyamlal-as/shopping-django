from django.urls import path
from api.v2.purchases import views

app_name = 'purchases'

urlpatterns = [
    path('<slug>',views.cart_api_view,name = "create-cart-api"),
    path('update/<slug>',views.cart_purchase_api,name='update-cart-api'),
]