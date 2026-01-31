from django.http import JsonResponse
from django.views.decorators.cache import cache_page
from django.views.decorators.http import require_GET
from .utils import (
    WeatherAPI, QuoteAPI, GitHubAPI, 
    UnsplashAPI, ExchangeRateAPI, NewsAPI
)
import json


@require_GET
@cache_page(60 * 15)  # Cache for 15 minutes
def get_weather(request):
    """
    API endpoint to get weather data
    """
    city = request.GET.get('city', 'London')
    country = request.GET.get('country', 'GB')
    
    weather_api = WeatherAPI()
    weather_data = weather_api.get_current_weather(city, country)
    
    return JsonResponse({
        'success': True,
        'data': weather_data,
        'source': 'OpenWeatherMap' if not weather_data.get('is_fallback') else 'Fallback'
    })


@require_GET
@cache_page(60 * 30)  # Cache for 30 minutes
def get_quote(request):
    """
    API endpoint to get random quote
    """
    quote_api = QuoteAPI()
    quote_data = quote_api.get_random_quote()
    
    return JsonResponse({
        'success': True,
        'data': quote_data,
        'source': quote_data.get('source', 'Fallback')
    })


@require_GET
@cache_page(60 * 60)  # Cache for 1 hour
def get_github_stats(request):
    """
    API endpoint to get GitHub stats
    """
    username = request.GET.get('username', 'octocat')
    
    github_api = GitHubAPI()
    user_stats = github_api.get_user_stats(username)
    user_repos = github_api.get_user_repos(username, 5)
    
    if user_stats:
        return JsonResponse({
            'success': True,
            'data': {
                'user': user_stats,
                'repositories': user_repos
            },
            'source': 'GitHub API'
        })
    
    return JsonResponse({
        'success': False,
        'error': 'Could not fetch GitHub data'
    }, status=404)


@require_GET
@cache_page(60 * 60)  # Cache for 1 hour
def get_random_image(request):
    """
    API endpoint to get random image
    """
    query = request.GET.get('query', 'nature')
    orientation = request.GET.get('orientation', 'landscape')
    
    unsplash_api = UnsplashAPI()
    image_data = unsplash_api.get_random_image(query, orientation)
    
    return JsonResponse({
        'success': True,
        'data': image_data,
        'source': 'Unsplash' if not image_data.get('is_fallback') else 'Fallback'
    })


@require_GET
@cache_page(60 * 60 * 24)  # Cache for 24 hours
def get_exchange_rates(request):
    """
    API endpoint to get exchange rates
    """
    base_currency = request.GET.get('base', 'USD')
    
    exchange_api = ExchangeRateAPI()
    exchange_data = exchange_api.get_exchange_rates(base_currency)
    
    return JsonResponse({
        'success': True,
        'data': exchange_data,
        'source': 'ExchangeRate-API' if not exchange_data.get('is_fallback') else 'Fallback'
    })


@require_GET
@cache_page(60 * 30)  # Cache for 30 minutes
def get_news(request):
    """
    API endpoint to get news
    """
    category = request.GET.get('category', 'technology')
    country = request.GET.get('country', 'us')
    max_results = int(request.GET.get('max', 5))
    
    news_api = NewsAPI()
    news_data = news_api.get_top_news(category, country, max_results)
    
    return JsonResponse({
        'success': True,
        'data': news_data,
        'source': 'GNews' if not news_data.get('is_fallback') else 'Fallback'
    })


@require_GET
def get_all_data(request):
    """
    Get all API data in one request
    """
    data = {}
    
    # Get weather
    weather_api = WeatherAPI()
    data['weather'] = weather_api.get_current_weather()
    
    # Get quote
    quote_api = QuoteAPI()
    data['quote'] = quote_api.get_random_quote()
    
    # Get GitHub stats (if username provided)
    github_username = request.GET.get('github_username')
    if github_username:
        github_api = GitHubAPI()
        data['github'] = {
            'user': github_api.get_user_stats(github_username),
            'repos': github_api.get_user_repos(github_username, 3)
        }
    
    # Get random image
    unsplash_api = UnsplashAPI()
    data['image'] = unsplash_api.get_random_image('technology')
    
    # Get exchange rates
    exchange_api = ExchangeRateAPI()
    data['exchange'] = exchange_api.get_exchange_rates()
    
    # Get news
    news_api = NewsAPI()
    data['news'] = news_api.get_top_news('technology', 'us', 3)
    
    return JsonResponse({
        'success': True,
        'data': data,
        'timestamp': datetime.now().isoformat()
    })