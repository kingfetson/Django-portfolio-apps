from django.urls import path
from . import views

app_name = 'menu'

urlpatterns = [
    path('api/menu/<str:menu_type>/', views.MenuAPIView.as_view(), name='api_menu'),
]