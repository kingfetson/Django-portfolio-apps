from rest_framework import serializers
from .models import Portfolio

class PortfolioSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    
    class Meta:
        model = Portfolio
        fields = '__all__'
        read_only_fields = ('user', 'created_at', 'updated_at')