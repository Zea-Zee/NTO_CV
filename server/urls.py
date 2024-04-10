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
    path('predict_front', views.predict_front, name='predict_front'),
    path('get_places_from_photo', views.predict_image_api_bridge, name='predict_image_api_bridge'),
    path('get_places_from_text', views.predict_text_api_bridge, name='predict_text_api_bridge'),
]
