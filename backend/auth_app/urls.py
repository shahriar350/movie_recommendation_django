from django.contrib import admin
from django.urls import path
from . import views

app_name = "auth"
urlpatterns = [
    path('csrf/', views.get_csrf_token),
    path('check/', views.CheckUser.as_view()),
    path('login/', views.LoginView.as_view(), name='login'),
    path('register/', views.RegisterView.as_view(), name='register'),
]
