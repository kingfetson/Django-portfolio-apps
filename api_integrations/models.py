from django.db import models
from django.utils import timezone

class APICache(models.Model):
    """
    Cache API responses to avoid rate limiting
    """
    api_name = models.CharField(max_length=100)
    endpoint = models.CharField(max_length=200)
    data = models.JSONField()
    expires_at = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        indexes = [
            models.Index(fields=['api_name', 'endpoint']),
            models.Index(fields=['expires_at']),
        ]
    
    def is_expired(self):
        return timezone.now() > self.expires_at
    
    def __str__(self):
        return f"{self.api_name} - {self.endpoint}"


class GitHubStats(models.Model):
    """
    Store GitHub statistics
    """
    username = models.CharField(max_length=100, unique=True)
    public_repos = models.IntegerField(default=0)
    followers = models.IntegerField(default=0)
    following = models.IntegerField(default=0)
    last_updated = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"GitHub: {self.username}"