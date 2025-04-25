from django.db import models
from companies.models import Company
from news.models import NewsArticle

class Prediction(models.Model):
    PREDICTION_CHOICES = [
        ('UP', 'Stock Price Will Increase'),
        ('DOWN', 'Stock Price Will Decrease'),
        ('NEUTRAL', 'No Significant Change'),
    ]
    
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='predictions')
    news_article = models.ForeignKey(NewsArticle, on_delete=models.CASCADE, related_name='predictions')
    prediction = models.CharField(max_length=10, choices=PREDICTION_CHOICES)
    confidence_score = models.FloatField()
    prediction_date = models.DateTimeField(auto_now_add=True)
    actual_movement = models.CharField(max_length=10, choices=PREDICTION_CHOICES, null=True, blank=True)
    actual_price_change = models.FloatField(null=True, blank=True)
    days_to_verify = models.IntegerField(default=3)  # Number of days after prediction to verify
    is_correct = models.BooleanField(null=True, blank=True)
    verified_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        ordering = ['-prediction_date']
    
    def __str__(self):
        return f"{self.company.ticker_symbol} - {self.prediction} ({self.prediction_date})"
