from django.urls import path
from . import views

app_name = 'skills'

urlpatterns = [
    path('', views.skill_list, name='list'),
    path('categories/', views.skill_categories, name='categories'),
    path('api/skills/', views.SkillListAPIView.as_view(), name='api_list'),
    path('api/skills/categories/', views.SkillCategoryAPIView.as_view(), name='api_categories'),
]
