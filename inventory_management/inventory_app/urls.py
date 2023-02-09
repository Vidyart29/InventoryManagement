from django.urls import path
from . import views


urlpatterns = [
    path("home", views.index, name="index"),
    path("", views.index, name="login"),
    path("signup", views.signupPage, name="signup"),
    path("login", views.loginPage, name="login"),
    path("logout", views.logoutPage, name="logout"),
]
