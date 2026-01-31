from django.urls import path
from . import views

app_name = 'portfolio'

urlpatterns = [
    path('', views.portfolio_home, name='home'),
    path('api/portfolio/', views.PortfolioAPIView.as_view(), name='api_portfolio'),
]