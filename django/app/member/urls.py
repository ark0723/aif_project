from django.urls import path
from .views import check_email, register_email

urlpatterns = [
    path("check_email/", check_email, name="check_email"),
    path("register_email/", register_email, name="register_email"),
]
