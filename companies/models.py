from django.db import models

# Create your models here.

class Company(models.Model):
    COUNTRY_CHOICES = [
        ('US', 'United States'),
        ('CN', 'China'),
        ('TW', 'Taiwan'),
    ]
    
    name = models.CharField(max_length=200)
    ticker_symbol = models.CharField(max_length=20, unique=True)
    country = models.CharField(max_length=2, choices=COUNTRY_CHOICES)
    industry = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name_plural = "Companies"
        ordering = ['name']
    
    def __str__(self):
        return f"{self.name} ({self.ticker_symbol})"
