from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django.shortcuts import render
from .models import Portfolio
from .serializers import PortfolioSerializer

def portfolio_home(request):
    portfolio = Portfolio.objects.first()
    return render(request, 'portfolio/home.html', {'portfolio': portfolio})

class PortfolioAPIView(APIView):
    permission_classes = [AllowAny]
    
    def get(self, request):
        portfolio = Portfolio.objects.first()
        serializer = PortfolioSerializer(portfolio)
        return Response(serializer.data)