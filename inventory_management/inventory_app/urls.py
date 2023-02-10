from django.urls import path
from . import views

urlpatterns = [
    path("home", views.index, name="index"),
    path("", views.index, name="login"),
    path("signup", views.signup, name="signup"),
    path("login", views.loginPage, name="login"),
    path("logout", views.logoutPage, name="logout"),
    path("products/<cat>", views.products, name="products"),
    path("products/", views.products, name="products"),
    path("categories/", views.categories, name="categories"),
    path("email/", views.email, name="email"),
    path("sendmail/", views.send_email, name="sendmail"),
]
