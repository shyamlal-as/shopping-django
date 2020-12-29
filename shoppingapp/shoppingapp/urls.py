"""shoppingapp URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from users.views import registration_view, logout_view, login_view
from store.views import profile
from django.conf import settings
from django.conf.urls.static import static

#from rest_framework_simplejwt.views import TokenObtainPairView, TokeRefreshView
from rest_framework_simplejwt import views as jwt_views

urlpatterns = [



    path('admin/', admin.site.urls),
    path('', include('store.urls')),
    path('cart/',include('purchases.urls')),

    path('profile/',profile,name='profile'),
    path('i18n/',include('django.conf.urls.i18n')),

    #User registration and Login

    path('register/',registration_view,name='register'),
    path('logout/',logout_view,name='logout'),
    path('login/',login_view,name='login'),

    #Rest Framework URL

    path('api/',include('shoppingapp.apiurls')),

    #JWT authorisation

    path('api/token', jwt_views.TokenObtainPairView.as_view()),
    path('api/token/refresh', jwt_views.TokenRefreshView.as_view()),

]+ static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)

