from django.urls import path,include


urlpatterns = [

    #Version 1
    path('v1/',include('shoppingapp.apiurls.apiv1urls')),

    #Version 2
    path('v12',include('shoppingapp.apiurls.apiv2urls')),
]