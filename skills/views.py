from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from .models import Skill, SkillCategory
from .serializers import SkillSerializer, SimpleSkillSerializer, SkillCategorySerializer

def skill_list(request):
    """List all skills grouped by category"""
    categories = SkillCategory.objects.filter(is_active=True).order_by('order')
    
    # Create a list of tuples (category, skills)
    categories_with_skills = []
    for category in categories:
        skills = category.skills.filter(is_active=True).order_by('resume_order')
        if skills.exists():
            categories_with_skills.append((category, skills))
    
    context = {
        'categories_with_skills': categories_with_skills,
    }
    return render(request, 'skills/list.html', context)


def skill_categories(request):
    """List skill categories"""
    categories = SkillCategory.objects.all().order_by('order')
    
    context = {
        'categories': categories,
    }
    return render(request, 'skills/categories.html', context)


# API Views
class SkillListAPIView(APIView):
    permission_classes = [AllowAny]
    
    def get(self, request):
        skills = Skill.objects.all().order_by('category__order', 'order')
        serializer = SimpleSkillSerializer(skills, many=True)
        return Response(serializer.data)


class SkillCategoryAPIView(APIView):
    permission_classes = [AllowAny]
    
    def get(self, request):
        categories = SkillCategory.objects.all().order_by('order')
        serializer = SkillCategorySerializer(categories, many=True)
        return Response(serializer.data)