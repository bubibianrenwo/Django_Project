from django.contrib import admin
from django.urls import path, include
from stapp import views

urlpatterns = [
    path('', views.start)
]
