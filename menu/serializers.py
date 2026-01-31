from rest_framework import serializers
from .models import MenuItem

class MenuItemSerializer(serializers.ModelSerializer):
    children = serializers.SerializerMethodField()
    
    class Meta:
        model = MenuItem
        fields = '__all__'
    
    def get_children(self, obj):
        children = obj.children.filter(is_active=True).order_by('order')
        return MenuItemSerializer(children, many=True).data