from django.urls import path
from . import views

urlpatterns = [
    path('', views.main, name='myrequest'),
    path('details/', views.myrequest, name='details'),
]