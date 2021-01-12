from django.urls import path, include


urlpatterns = [
    path('v1/store/',include('store.api.v1.urls')),
    path('v1/purchase/',include('purchases.api.v1.urls')),
    path('v1/users/',include('users.api.v1.urls')),
    path('v2/store/',include('store.api.v2.urls')),
    path('v2/purchase/',include('purchases.api.v2.urls')),
    path('v2/users/',include('users.api.v2.urls')),

    ]