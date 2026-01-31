import os
import requests
import json
from datetime import datetime, timedelta
from django.utils import timezone
from django.core.cache import cache
from .models import APICache
import logging

logger = logging.getLogger(__name__)

class APIHandler:
    """
    Base class for API integrations with caching
    """
    
    def __init__(self, api_name, cache_duration_minutes=30):
        self.api_name = api_name
        self.cache_duration = cache_duration_minutes
    
    def get_cached_response(self, endpoint, params=None):
        """
        Get cached response or fetch from API
        """
        cache_key = f"{self.api_name}:{endpoint}:{json.dumps(params or {}, sort_keys=True)}"
        
        # Check Django cache first
        cached_data = cache.get(cache_key)
        if cached_data:
            logger.info(f"Cache hit for {cache_key}")
            return cached_data
        
        # Check database cache
        try:
            db_cache = APICache.objects.filter(
                api_name=self.api_name,
                endpoint=endpoint,
                expires_at__gt=timezone.now()
            ).first()
            
            if db_cache:
                logger.info(f"Database cache hit for {self.api_name}:{endpoint}")
                cache.set(cache_key, db_cache.data, self.cache_duration * 60)
                return db_cache.data
        except Exception as e:
            logger.error(f"Error checking database cache: {e}")
        
        return None
    
    def cache_response(self, endpoint, data, params=None):
        """
        Cache API response
        """
        cache_key = f"{self.api_name}:{endpoint}:{json.dumps(params or {}, sort_keys=True)}"
        
        # Cache in Django cache
        cache.set(cache_key, data, self.cache_duration * 60)
        
        # Cache in database for persistence
        try:
            APICache.objects.create(
                api_name=self.api_name,
                endpoint=endpoint,
                data=data,
                expires_at=timezone.now() + timedelta(minutes=self.cache_duration)
            )
        except Exception as e:
            logger.error(f"Error caching to database: {e}")
        
        return data
    
    def make_request(self, url, endpoint, params=None, headers=None):
        """
        Make API request with caching
        """
        # Check cache first
        cached_data = self.get_cached_response(endpoint, params)
        if cached_data:
            return cached_data
        
        # Make API request
        try:
            response = requests.get(
                url,
                params=params,
                headers=headers,
                timeout=10
            )
            response.raise_for_status()
            data = response.json()
            
            # Cache the response
            self.cache_response(endpoint, data, params)
            
            return data
        except requests.exceptions.RequestException as e:
            logger.error(f"API request failed for {self.api_name}: {e}")
            return None


class WeatherAPI(APIHandler):
    """
    OpenWeatherMap API integration
    Free tier: 60 calls/minute, 1,000,000 calls/month
    """
    
    def __init__(self):
        super().__init__('weather', cache_duration_minutes=30)
        self.api_key = os.getenv('OPENWEATHER_API_KEY', '')
        self.base_url = "https://api.openweathermap.org/data/2.5"
    
    def get_current_weather(self, city="London", country_code="GB"):
        """
        Get current weather for a city
        """
        if not self.api_key:
            return self._get_fallback_weather()
        
        endpoint = "weather"
        params = {
            'q': f"{city},{country_code}",
            'appid': self.api_key,
            'units': 'metric'  # Celsius
        }
        
        data = self.make_request(
            f"{self.base_url}/{endpoint}",
            endpoint,
            params
        )
        
        if data:
            return {
                'city': data.get('name', city),
                'country': data.get('sys', {}).get('country', country_code),
                'temperature': round(data.get('main', {}).get('temp', 0)),
                'feels_like': round(data.get('main', {}).get('feels_like', 0)),
                'humidity': data.get('main', {}).get('humidity', 0),
                'description': data.get('weather', [{}])[0].get('description', ''),
                'icon': data.get('weather', [{}])[0].get('icon', '01d'),
                'icon_url': f"https://openweathermap.org/img/wn/{data.get('weather', [{}])[0].get('icon', '01d')}@2x.png",
                'wind_speed': data.get('wind', {}).get('speed', 0),
                'timestamp': datetime.fromtimestamp(data.get('dt', 0)).isoformat() if data.get('dt') else None
            }
        
        return self._get_fallback_weather()
    
    def _get_fallback_weather(self):
        """Fallback weather data when API is not available"""
        return {
            'city': 'London',
            'country': 'GB',
            'temperature': 18,
            'feels_like': 19,
            'humidity': 65,
            'description': 'Partly cloudy',
            'icon': '02d',
            'icon_url': 'https://openweathermap.org/img/wn/02d@2x.png',
            'wind_speed': 3.5,
            'timestamp': datetime.now().isoformat(),
            'is_fallback': True
        }


class QuoteAPI(APIHandler):
    """
    Free Quotes API
    Multiple sources available
    """
    
    def __init__(self):
        super().__init__('quotes', cache_duration_minutes=60)
    
    def get_random_quote(self):
        """
        Get a random inspirational quote
        """
        endpoints = [
            {
                'name': 'quotable',
                'url': 'https://api.quotable.io/random',
                'parser': self._parse_quotable
            },
            {
                'name': 'zenquotes',
                'url': 'https://zenquotes.io/api/random',
                'parser': self._parse_zenquotes
            },
            {
                'name': 'typefit',
                'url': 'https://type.fit/api/quotes',
                'parser': self._parse_typefit
            }
        ]
        
        for endpoint in endpoints:
            try:
                data = self.make_request(endpoint['url'], endpoint['name'])
                if data:
                    quote_data = endpoint['parser'](data)
                    if quote_data:
                        return quote_data
            except Exception as e:
                logger.error(f"Error fetching quote from {endpoint['name']}: {e}")
                continue
        
        # Fallback quote
        return self._get_fallback_quote()
    
    def _parse_quotable(self, data):
        """Parse quotable.io response"""
        return {
            'quote': data.get('content', ''),
            'author': data.get('author', 'Unknown'),
            'source': 'quotable.io',
            'tags': data.get('tags', [])
        }
    
    def _parse_zenquotes(self, data):
        """Parse zenquotes.io response"""
        if isinstance(data, list) and len(data) > 0:
            return {
                'quote': data[0].get('q', ''),
                'author': data[0].get('a', 'Unknown'),
                'source': 'zenquotes.io'
            }
        return None
    
    def _parse_typefit(self, data):
        """Parse type.fit response"""
        import random
        if isinstance(data, list) and len(data) > 0:
            quote = random.choice(data)
            return {
                'quote': quote.get('text', ''),
                'author': quote.get('author', 'Unknown').replace(', type.fit', ''),
                'source': 'type.fit'
            }
        return None
    
    def _get_fallback_quote(self):
        """Fallback quotes"""
        fallback_quotes = [
            {
                'quote': 'The only way to do great work is to love what you do.',
                'author': 'Steve Jobs',
                'source': 'Fallback'
            },
            {
                'quote': 'Innovation distinguishes between a leader and a follower.',
                'author': 'Steve Jobs',
                'source': 'Fallback'
            },
            {
                'quote': 'The future belongs to those who believe in the beauty of their dreams.',
                'author': 'Eleanor Roosevelt',
                'source': 'Fallback'
            }
        ]
        import random
        return random.choice(fallback_quotes)


class GitHubAPI(APIHandler):
    """
    GitHub API integration
    No API key needed for basic user data (60 requests/hour)
    """
    
    def __init__(self):
        super().__init__('github', cache_duration_minutes=60)
        self.base_url = "https://api.github.com"
    
    def get_user_stats(self, username):
        """
        Get GitHub user statistics
        """
        endpoint = f"users/{username}"
        
        data = self.make_request(
            f"{self.base_url}/{endpoint}",
            endpoint
        )
        
        if data:
            return {
                'username': data.get('login', username),
                'name': data.get('name', ''),
                'avatar_url': data.get('avatar_url', ''),
                'public_repos': data.get('public_repos', 0),
                'public_gists': data.get('public_gists', 0),
                'followers': data.get('followers', 0),
                'following': data.get('following', 0),
                'created_at': data.get('created_at', ''),
                'updated_at': data.get('updated_at', ''),
                'bio': data.get('bio', ''),
                'blog': data.get('blog', ''),
                'company': data.get('company', ''),
                'location': data.get('location', ''),
                'hireable': data.get('hireable', False)
            }
        
        return None
    
    def get_user_repos(self, username, limit=5):
        """
        Get user's repositories
        """
        endpoint = f"users/{username}/repos"
        params = {
            'sort': 'updated',
            'direction': 'desc',
            'per_page': limit
        }
        
        data = self.make_request(
            f"{self.base_url}/{endpoint}",
            endpoint,
            params
        )
        
        if data and isinstance(data, list):
            repos = []
            for repo in data[:limit]:
                repos.append({
                    'name': repo.get('name', ''),
                    'full_name': repo.get('full_name', ''),
                    'description': repo.get('description', ''),
                    'html_url': repo.get('html_url', ''),
                    'language': repo.get('language', ''),
                    'stars': repo.get('stargazers_count', 0),
                    'forks': repo.get('forks_count', 0),
                    'updated_at': repo.get('updated_at', ''),
                    'is_fork': repo.get('fork', False)
                })
            return repos
        
        return []


class UnsplashAPI(APIHandler):
    """
    Unsplash API for random images
    Free tier: 50 requests/hour
    Requires access key (free from unsplash.com/developers)
    """
    
    def __init__(self):
        super().__init__('unsplash', cache_duration_minutes=60)
        self.access_key = os.getenv('UNSPLASH_ACCESS_KEY', '')
        self.base_url = "https://api.unsplash.com"
    
    def get_random_image(self, query="nature", orientation="landscape"):
        """
        Get a random image from Unsplash
        """
        if not self.access_key:
            return self._get_fallback_image(query)
        
        endpoint = "photos/random"
        params = {
            'query': query,
            'orientation': orientation,
            'count': 1
        }
        headers = {
            'Authorization': f'Client-ID {self.access_key}'
        }
        
        data = self.make_request(
            f"{self.base_url}/{endpoint}",
            endpoint,
            params,
            headers
        )
        
        if data and isinstance(data, list) and len(data) > 0:
            image_data = data[0]
            return {
                'id': image_data.get('id', ''),
                'url': image_data.get('urls', {}).get('regular', ''),
                'thumb_url': image_data.get('urls', {}).get('thumb', ''),
                'download_url': image_data.get('links', {}).get('download', ''),
                'description': image_data.get('description', image_data.get('alt_description', '')),
                'photographer': image_data.get('user', {}).get('name', 'Unknown'),
                'photographer_url': image_data.get('user', {}).get('links', {}).get('html', ''),
                'photographer_username': image_data.get('user', {}).get('username', ''),
                'color': image_data.get('color', '#667eea'),
                'width': image_data.get('width', 1200),
                'height': image_data.get('height', 800)
            }
        
        return self._get_fallback_image(query)
    
    def _get_fallback_image(self, query):
        """Fallback image data"""
        fallback_images = {
            'nature': 'https://images.unsplash.com/photo-1501854140801-50d01698950b?ixlib=rb-4.0.3&auto=format&fit=crop&w=1200&q=80',
            'technology': 'https://images.unsplash.com/photo-1518709268805-4e9042af2176?ixlib=rb-4.0.3&auto=format&fit=crop&w=1200&q=80',
            'food': 'https://images.unsplash.com/photo-1565958011703-44f9829ba187?ixlib=rb-4.0.3&auto=format&fit=crop&w=1200&q=80',
            'default': 'https://images.unsplash.com/photo-1550684376-efcbd6e3f031?ixlib=rb-4.0.3&auto=format&fit=crop&w=1200&q=80'
        }
        
        image_url = fallback_images.get(query.lower(), fallback_images['default'])
        
        return {
            'url': image_url,
            'thumb_url': image_url,
            'description': f'Beautiful {query} image',
            'photographer': 'Unsplash Community',
            'photographer_url': 'https://unsplash.com',
            'color': '#667eea',
            'is_fallback': True
        }


class ExchangeRateAPI(APIHandler):
    """
    Free currency exchange rate API
    Using exchangerate-api.com (1,500 requests/month free)
    """
    
    def __init__(self):
        super().__init__('exchange', cache_duration_minutes=1440)  # 24 hours
        self.api_key = os.getenv('EXCHANGE_RATE_API_KEY', '')
        self.base_url = "https://v6.exchangerate-api.com/v6"
    
    def get_exchange_rates(self, base_currency='USD'):
        """
        Get exchange rates for a base currency
        """
        if not self.api_key:
            return self._get_fallback_rates(base_currency)
        
        endpoint = f"latest/{base_currency}"
        
        data = self.make_request(
            f"{self.base_url}/{self.api_key}/{endpoint}",
            endpoint
        )
        
        if data and data.get('result') == 'success':
            return {
                'base_currency': data.get('base_code', base_currency),
                'last_updated': datetime.fromtimestamp(data.get('time_last_update_unix', 0)).isoformat() if data.get('time_last_update_unix') else None,
                'rates': data.get('conversion_rates', {}),
                'supported_codes': self._get_currency_codes()
            }
        
        return self._get_fallback_rates(base_currency)
    
    def _get_currency_codes(self):
        """Get list of currency codes"""
        return {
            'USD': 'US Dollar',
            'EUR': 'Euro',
            'GBP': 'British Pound',
            'JPY': 'Japanese Yen',
            'CAD': 'Canadian Dollar',
            'AUD': 'Australian Dollar',
            'CHF': 'Swiss Franc',
            'CNY': 'Chinese Yuan',
            'INR': 'Indian Rupee',
        }
    
    def _get_fallback_rates(self, base_currency):
        """Fallback exchange rates"""
        rates = {
            'USD': 1.0,
            'EUR': 0.92,
            'GBP': 0.79,
            'JPY': 148.0,
            'CAD': 1.35,
            'AUD': 1.52,
            'CHF': 0.88,
            'CNY': 7.18,
            'INR': 83.0,
        }
        
        # Convert to base currency if not USD
        if base_currency != 'USD' and base_currency in rates:
            base_rate = rates[base_currency]
            converted_rates = {}
            for currency, rate in rates.items():
                converted_rates[currency] = round(rate / base_rate, 4)
            rates = converted_rates
        
        return {
            'base_currency': base_currency,
            'last_updated': datetime.now().isoformat(),
            'rates': rates,
            'supported_codes': self._get_currency_codes(),
            'is_fallback': True
        }


class NewsAPI(APIHandler):
    """
    News API integration
    Using GNews API (free tier available)
    """
    
    def __init__(self):
        super().__init__('news', cache_duration_minutes=30)
        self.api_key = os.getenv('GNEWS_API_KEY', '')
        self.base_url = "https://gnews.io/api/v4"
    
    def get_top_news(self, category='general', country='us', max_results=5):
        """
        Get top news headlines
        """
        if not self.api_key:
            return self._get_fallback_news()
        
        endpoint = "top-headlines"
        params = {
            'category': category,
            'country': country,
            'max': max_results,
            'apikey': self.api_key
        }
        
        data = self.make_request(
            f"{self.base_url}/{endpoint}",
            endpoint,
            params
        )
        
        if data and data.get('articles'):
            articles = []
            for article in data['articles'][:max_results]:
                articles.append({
                    'title': article.get('title', ''),
                    'description': article.get('description', ''),
                    'content': article.get('content', ''),
                    'url': article.get('url', ''),
                    'image': article.get('image', ''),
                    'published_at': article.get('publishedAt', ''),
                    'source': article.get('source', {}).get('name', ''),
                })
            return {
                'category': category,
                'country': country,
                'total_articles': data.get('totalArticles', 0),
                'articles': articles
            }
        
        return self._get_fallback_news()
    
    def _get_fallback_news(self):
        """Fallback news data"""
        return {
            'category': 'general',
            'country': 'us',
            'total_articles': 3,
            'articles': [
                {
                    'title': 'Technology Advances in AI Development',
                    'description': 'Recent breakthroughs in artificial intelligence are changing how we interact with technology.',
                    'url': '#',
                    'image': 'https://images.unsplash.com/photo-1677442136019-21780ecad995?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80',
                    'published_at': datetime.now().isoformat(),
                    'source': 'Tech News'
                },
                {
                    'title': 'Sustainable Energy Solutions Gain Momentum',
                    'description': 'Global initiatives focus on renewable energy sources to combat climate change.',
                    'url': '#',
                    'image': 'https://images.unsplash.com/photo-1466611653911-95081537e5b7?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80',
                    'published_at': datetime.now().isoformat(),
                    'source': 'Environment Daily'
                },
                {
                    'title': 'Web Development Trends for 2024',
                    'description': 'New frameworks and tools are shaping the future of web development.',
                    'url': '#',
                    'image': 'https://images.unsplash.com/photo-1555066931-4365d14bab8c?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80',
                    'published_at': datetime.now().isoformat(),
                    'source': 'Dev Weekly'
                }
            ],
            'is_fallback': True
        }