from django.urls import path
from django.shortcuts import redirect
from . import views
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path, include


urlpatterns = [
    path('', lambda request: views.custom_redirect('upload/')),
    path('upload/', views.upload_image, name='upload_image'),
    path('image_search/', views.image, name='image_search'),
    path('text_search/', views.text, name='text_search'),
    path('fetch_otp/', views.fetch_OTP, name='fetch_otp'),
]
