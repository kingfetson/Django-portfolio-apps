from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from .models import MenuItem
from .serializers import MenuItemSerializer

class MenuAPIView(APIView):
    permission_classes = [AllowAny]
    
    def get(self, request, menu_type):
        menu_items = MenuItem.objects.filter(
            menu_type=menu_type,
            is_active=True,
            parent__isnull=True
        ).order_by('order')
        serializer = MenuItemSerializer(menu_items, many=True)
        return Response(serializer.data)