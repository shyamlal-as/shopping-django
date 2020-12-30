from django.urls import path,include


urlpatterns = [

    path('store/',include('apps.store.api.v2.urls')),
    path('cart/',include('apps.purchases.api.v2.urls')),

]