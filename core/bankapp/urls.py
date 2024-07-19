from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('transfer/', views.transfer, name='transfer'),
    path('deposit/', views.deposit, name='deposit'),
    
]