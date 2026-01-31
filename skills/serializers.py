from rest_framework import serializers
from .models import Skill, SkillCategory

class SkillCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = SkillCategory
        fields = ['id', 'name', 'description', 'icon_class', 'order']


class SkillSerializer(serializers.ModelSerializer):
    category = SkillCategorySerializer(read_only=True)
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=SkillCategory.objects.all(),
        source='category',
        write_only=True,
        required=False
    )
    proficiency_stars = serializers.IntegerField(read_only=True)
    
    class Meta:
        model = Skill
        fields = [
            'id', 'name', 'category', 'category_id', 'skill_level',
            'proficiency', 'proficiency_stars', 'icon_class', 'color',
            'years_of_experience', 'is_featured', 'order', 'description',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']


class SimpleSkillSerializer(serializers.ModelSerializer):
    """Simplified serializer for listings"""
    category_name = serializers.CharField(source='category.name', read_only=True)
    
    class Meta:
        model = Skill
        fields = [
            'id', 'name', 'category_name', 'skill_level',
            'proficiency', 'icon_class', 'color', 'is_featured'
        ]