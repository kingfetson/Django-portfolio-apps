# dishes/views.py
from django.shortcuts import render
from landing.models import Portfolio  # or portfolio.models import Portfolio
from .models import Dish

def dish_list(request):
    dishes = Dish.objects.all()
    portfolio = Portfolio.objects.first()  # Get portfolio for header
    
    context = {
        'dishes': dishes,
        'portfolio': portfolio,
    }
    return render(request, 'dishes/list.html', context)