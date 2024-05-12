from django.urls import path
from . import views
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path("check_email/", views.check_email, name="check_email"),
    path("register_email/", views.register_email, name="register_email"),
    path("", views.Users.as_view()),
    path("myinfo", views.MyInfo.as_view()),
    path("<int:member_id>", views.UserDetail.as_view()),
    # authentication
    path("getToken", views.CustomAuthToken.as_view()),
    path("login", views.Login.as_view()),
    path("logout", views.Logout.as_view()),
    path("jwt-login", views.JWTLogin.as_view()),  # jwt authentication
]
