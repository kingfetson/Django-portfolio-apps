from django.shortcuts import render, get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from .models import Project, ProjectCategory
from .serializers import ProjectSerializer, SimpleProjectSerializer, ProjectCategorySerializer

def project_list(request):
    """List all projects"""
    projects = Project.objects.filter(is_published=True).order_by('-is_featured', '-created_at')
    categories = ProjectCategory.objects.all().order_by('order')
    
    context = {
        'projects': projects,
        'categories': categories,
    }
    return render(request, 'projects/list.html', context)


def project_detail(request, slug):
    """Project detail view"""
    project = get_object_or_404(Project, slug=slug, is_published=True)
    
    # Increment view count
    project.views += 1
    project.save()
    
    context = {
        'project': project,
    }
    return render(request, 'projects/detail.html', context)


def project_category(request, category_slug):
    """Projects by category"""
    category = get_object_or_404(ProjectCategory, slug=category_slug)
    projects = Project.objects.filter(
        category=category, 
        is_published=True
    ).order_by('-is_featured', '-created_at')
    
    context = {
        'category': category,
        'projects': projects,
    }
    return render(request, 'projects/category.html', context)


# API Views
class ProjectListAPIView(APIView):
    permission_classes = [AllowAny]
    
    def get(self, request):
        projects = Project.objects.filter(is_published=True).order_by('-is_featured', '-created_at')
        serializer = SimpleProjectSerializer(projects, many=True)
        return Response(serializer.data)


class ProjectDetailAPIView(APIView):
    permission_classes = [AllowAny]
    
    def get(self, request, slug):
        project = get_object_or_404(Project, slug=slug, is_published=True)
        serializer = ProjectSerializer(project)
        return Response(serializer.data)


class ProjectCategoryAPIView(APIView):
    permission_classes = [AllowAny]
    
    def get(self, request):
        categories = ProjectCategory.objects.all().order_by('order')
        serializer = ProjectCategorySerializer(categories, many=True)
        return Response(serializer.data)