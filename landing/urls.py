from django.urls import path
from . import views

app_name = 'landing'

urlpatterns = [
    path('', views.portfolio_home, name='home'),
    path('about/', views.about_page, name='about'),
    path('contact/', views.contact_page, name='contact'),
    path('api/landing-data/', views.LandingDataAPIView.as_view(), name='api_landing_data'),
    path('debug/images/', views.image_debug, name='image_debug'),  # This was outside the list
]