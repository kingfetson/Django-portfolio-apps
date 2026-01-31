from django.urls import path
from . import views

app_name = 'travel'

urlpatterns = [
    path('', views.travel_home, name='home'),
    path('destinations/', views.destination_list, name='destinations'),
    path('destinations/<slug:slug>/', views.destination_detail, name='destination_detail'),
    path('trips/', views.trip_list, name='trips'),
    path('trips/<slug:slug>/', views.trip_detail, name='trip_detail'),
    path('tips/', views.travel_tips, name='tips'),
    path('wishlist/', views.my_wishlist, name='wishlist'),
]
