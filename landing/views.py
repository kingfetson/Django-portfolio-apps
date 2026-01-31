from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.http import require_GET
from django.contrib.auth.decorators import login_required
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
import requests
import json
from .models import Portfolio, Project, Skill, Dish, MenuItem

def portfolio_home(request):
    # Get the first portfolio or create a default one
    portfolio = Portfolio.objects.first()
    
    context = {
        'portfolio': portfolio,
        'featured_projects': Project.objects.filter(featured=True).order_by('order')[:4] if portfolio else [],
        'featured_skills': Skill.objects.filter(featured=True).order_by('order')[:6] if portfolio else [],
        'featured_dishes': Dish.objects.filter(featured=True).order_by('order')[:4] if portfolio else [],
        'header_menu': MenuItem.objects.filter(portfolio=portfolio).order_by('order') if portfolio else [],
        'enable_weather_widget': portfolio.enable_weather_widget if portfolio else True,
        'enable_quote_widget': portfolio.enable_quote_widget if portfolio else True,
        'enable_github_widget': portfolio.enable_github_widget if portfolio else True,
    }
    #return render(request, 'portfolio/portfolio.html', context)
    return render(request, 'landing/index.html', context)


def about_page(request):
    """About page view"""
    portfolio = Portfolio.objects.first()
    return render(request, 'landing/about.html', {'portfolio': portfolio})


def contact_page(request):
    """Contact page view"""
    portfolio = Portfolio.objects.first()
    return render(request, 'landing/contact.html', {'portfolio': portfolio})


def image_debug(request):
    """Image debug view"""
    portfolio = Portfolio.objects.first()
    return render(request, 'landing/image_debug.html', {'portfolio': portfolio})


class LandingDataAPIView(APIView):
    """API view for landing data"""
    def get(self, request):
        portfolio = Portfolio.objects.first()
        # If you don't have a serializer yet, use a simple dictionary
        if portfolio:
            data = {
                'id': portfolio.id,
                'name': portfolio.name,
                'title': portfolio.title,
                'bio': portfolio.bio,
                'email': portfolio.email,
                'phone': portfolio.phone,
                'location': portfolio.location,
                # Add other fields as needed
            }
        else:
            data = {}
        return Response(data)


@require_GET
def weather_api(request):
    city = request.GET.get('city', 'London')
    country = request.GET.get('country', 'GB')
    
    # Using OpenWeatherMap API (you need an API key)
    api_key = getattr(settings, 'OPENWEATHER_API_KEY', '')
    
    if not api_key:
        # Return mock data if no API key
        return JsonResponse({
            'success': True,
            'data': {
                'city': city,
                'country': country,
                'temperature': 18,
                'feels_like': 17,
                'humidity': 65,
                'wind_speed': 3.5,
                'description': 'Partly cloudy',
                'icon_url': 'https://openweathermap.org/img/wn/03d@2x.png'
            }
        })
    
    try:
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city},{country}&appid={api_key}&units=metric"
        response = requests.get(url, timeout=5)
        data = response.json()
        
        if response.status_code == 200:
            return JsonResponse({
                'success': True,
                'data': {
                    'city': city,
                    'country': country,
                    'temperature': data['main']['temp'],
                    'feels_like': data['main']['feels_like'],
                    'humidity': data['main']['humidity'],
                    'wind_speed': data['wind']['speed'],
                    'description': data['weather'][0]['description'].title(),
                    'icon_url': f"https://openweathermap.org/img/wn/{data['weather'][0]['icon']}@2x.png"
                }
            })
        else:
            return JsonResponse({
                'success': False,
                'error': 'Weather data not available'
            })
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        })


@require_GET
def quote_api(request):
    try:
        # Using Quotable API
        response = requests.get('https://api.quotable.io/random', timeout=5)
        data = response.json()
        
        return JsonResponse({
            'success': True,
            'data': {
                'quote': data['content'],
                'author': data['author'],
                'source': 'Quotable API'
            }
        })
    except:
        # Fallback quotes
        fallback_quotes = [
            {"quote": "The only way to do great work is to love what you do.", "author": "Steve Jobs"},
            {"quote": "Innovation distinguishes between a leader and a follower.", "author": "Steve Jobs"},
            {"quote": "The future belongs to those who believe in the beauty of their dreams.", "author": "Eleanor Roosevelt"},
        ]
        import random
        quote = random.choice(fallback_quotes)
        return JsonResponse({
            'success': True,
            'data': {
                'quote': quote['quote'],
                'author': quote['author'],
                'source': 'Fallback'
            }
        })


@require_GET
def github_api(request):
    username = request.GET.get('username', '')
    
    if not username:
        return JsonResponse({
            'success': False,
            'error': 'No username provided'
        })
    
    try:
        # Get user data
        user_response = requests.get(f'https://api.github.com/users/{username}', timeout=5)
        user_data = user_response.json()
        
        # Get repositories
        repos_response = requests.get(f'https://api.github.com/users/{username}/repos', timeout=5)
        repos_data = repos_response.json()
        
        return JsonResponse({
            'success': True,
            'data': {
                'user': {
                    'public_repos': user_data.get('public_repos', 0),
                    'followers': user_data.get('followers', 0),
                    'following': user_data.get('following', 0),
                    'public_gists': user_data.get('public_gists', 0),
                },
                'repositories': [
                    {
                        'name': repo.get('name'),
                        'description': repo.get('description'),
                        'html_url': repo.get('html_url'),
                        'language': repo.get('language'),
                    }
                    for repo in repos_data[:5]  # Limit to 5 repos
                ]
            }
        })
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        })
