from django.urls import path

from . import views

urlpatterns = [
    path('load-cities/', views.load_cities, name='load_cities'),
    path('load-weather/', views.load_weather, name='load_weather')
]