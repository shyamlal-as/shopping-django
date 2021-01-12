
from django.urls import path
from .views import registration_view
#from rest_framework.authtoken.views import  obtain_auth_token
from rest_framework_simplejwt import views as jwt_views


app_name="users"

urlpatterns = [
    path('register/',registration_view, name="register"),
    #path('login/',obtain_auth_token, name="login"),
    path('login/',jwt_views.TokenObtainPairView.as_view(), name="login"),
]