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
from django.conf.urls.i18n import i18n_patterns
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('i18n/',include('django.conf.urls.i18n')),
    path('admin/', admin.site.urls),
]

urlpatterns += [
    path('', include('store.urls')),
    path('purchases/', include('purchases.urls')),
    path('users/', include('users.urls')),
    #path('cart/',include('purchases.urls')),
    path('profile/',profile,name='profile'),

    path('register/',registration_view,name='register'),
    path('logout/',logout_view,name='logout'),
    path('login/',login_view,name='login'),

    #Rest Framework URLs

    #path('api/',include('api.urls', 'apis')),
    path('api/token',TokenObtainPairView.as_view()),
    path('api/token/refresh',TokenRefreshView.as_view()),


]+ static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)

