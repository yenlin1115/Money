from django.db import models
from companies.models import Company

class NewsArticle(models.Model):
    SOURCE_CHOICES = [
        ('GDELT', 'GDELT'),
        ('NEWSAPI', 'NewsAPI'),
        ('OTHER', 'Other'),
    ]
    
    title = models.CharField(max_length=500)
    content = models.TextField()
    source = models.CharField(max_length=20, choices=SOURCE_CHOICES)
    url = models.URLField(max_length=500)
    published_date = models.DateTimeField()
    sentiment_score = models.FloatField(null=True, blank=True)
    sentiment_label = models.CharField(max_length=20, null=True, blank=True)
    related_companies = models.ManyToManyField(Company, related_name='news_articles')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-published_date']
    
    def __str__(self):
        return f"{self.title} ({self.source})"
