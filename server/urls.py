from django.urls import path

from . import views
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path, include
from .views import index


urlpatterns = [
    path('', index, name="index"),
    path('upload/', views.upload_image, name='upload_image'),
    path('image_search/', views.image, name='image_search'),
    path('text_search/', views.text, name='text_search'),
    path('<str:lat1>,<str:long1>,<str:lat2>,<str:long2>',views.showroute,name='showroute'),
]