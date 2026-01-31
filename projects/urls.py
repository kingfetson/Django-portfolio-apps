from django.urls import path
from . import views

app_name = 'projects'

urlpatterns = [
    path('', views.project_list, name='list'),
    path('<slug:slug>/', views.project_detail, name='detail'),
    path('category/<slug:category_slug>/', views.project_category, name='category'),
    path('api/projects/', views.ProjectListAPIView.as_view(), name='api_list'),
    path('api/projects/<slug:slug>/', views.ProjectDetailAPIView.as_view(), name='api_detail'),
]
