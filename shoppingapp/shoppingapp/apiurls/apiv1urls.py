from django.urls import path,include


urlpatterns = [
    
    path('store/',include('apps.store.api.v1.urls')),
    path('cart/',include('apps.purchases.api.v1.urls')),
    path('users/',include('apps.users.api.v1.urls')),

]



