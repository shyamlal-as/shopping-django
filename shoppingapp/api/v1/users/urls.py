from django.urls import path
from api.v1.users.views import registration_view
from rest_framework.authtoken.views import  obtain_auth_token

app_name="users"

urlpatterns = [
    path('register/',registration_view, name="register"),
    path('login/',obtain_auth_token, name="login"),
]
