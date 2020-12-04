from django.contrib import admin
from django.urls import path, include
from users.views import registration_view, logout_view, login_view
from purchase.views import purchases
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.urlpatterns import format_suffix_patterns
from store import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('store.urls')),
    path('register/',registration_view,name='register'),
    path('logout/',logout_view,name='logout'),
    path('login/',login_view,name='login'),
    path('purchase/',include('purchase.urls')),
    path('shipping/',include('shipping.urls')),
    path('productss/',views.productList.as_view()),
]

urlpatterns+=static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)

