from django.urls import path
from . import views

app_name = 'api_integrations'

urlpatterns = [
    path('weather/', views.get_weather, name='weather'),
    path('quote/', views.get_quote, name='quote'),
    path('github/', views.get_github_stats, name='github'),
    path('image/', views.get_random_image, name='image'),
    path('exchange/', views.get_exchange_rates, name='exchange'),
    path('news/', views.get_news, name='news'),
    path('all/', views.get_all_data, name='all_data'),
]