from django.urls import path, re_path, include
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
    path("", views.HomeTemplateView.as_view(), name='home'),
    path("sign-up/", views.RegisterView.as_view(), name='register'),
    path("login/", views.login_page, name="login"),
    path("logout/", views.logout_page, name="logout"),
]
    
