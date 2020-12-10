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


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('store.urls')),
    #path('cart/',include('purchases.urls')),
    path('profile/',profile,name='profile'),

    path('register/',registration_view,name='register'),
    path('logout/',logout_view,name='logout'),
    path('login/',login_view,name='login'),

    #Rest Framework URLs
    path('api/store/',include('store.api.urls', 'product_api')),
    path('api/users/',include('users.api.urls', 'users_api')),
    path('api/cart/',include('purchases.api.urls','cart_api'))

]+ static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)

