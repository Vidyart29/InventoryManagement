from django.urls import path
from inventory_app import views

urlpatterns = [
    path('', views.inventory_app, name=''),
]