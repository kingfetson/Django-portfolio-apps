from django import template
import urllib.parse

register = template.Library()

@register.filter
def fix_image_url(url):
    """Fix image URL encoding issues"""
    if url:
        # Parse and reconstruct URL to handle special characters
        return urllib.parse.quote(url, safe='/:')
    return url

@register.filter
def get_image_filename(url):
    """Extract filename from URL"""
    if url:
        return url.split('/')[-1]
    return ''
