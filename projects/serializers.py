from rest_framework import serializers
from .models import Project, ProjectCategory

class ProjectCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectCategory
        fields = ['id', 'name', 'slug', 'description', 'icon_class']


class ProjectSerializer(serializers.ModelSerializer):
    category = ProjectCategorySerializer(read_only=True)
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=ProjectCategory.objects.all(),
        source='category',
        write_only=True,
        required=False
    )
    skills = serializers.StringRelatedField(many=True, read_only=True)
    duration = serializers.CharField(read_only=True)
    
    class Meta:
        model = Project
        fields = [
            'id', 'title', 'slug', 'short_description', 'full_description',
            'category', 'category_id', 'project_type', 'status',
            'is_featured', 'is_published', 'start_date', 'end_date',
            'github_url', 'live_url', 'demo_url', 'documentation_url',
            'featured_image', 'thumbnail', 'skills', 'views',
            'created_at', 'updated_at', 'duration'
        ]
        read_only_fields = ['slug', 'views', 'created_at', 'updated_at']


class SimpleProjectSerializer(serializers.ModelSerializer):
    """Simplified serializer for listings"""
    category_name = serializers.CharField(source='category.name', read_only=True)
    
    class Meta:
        model = Project
        fields = [
            'id', 'title', 'slug', 'short_description',
            'category_name', 'project_type', 'is_featured',
            'featured_image', 'thumbnail', 'views'
        ]