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

class StockData(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='stock_data')
    date = models.DateField()
    open_price = models.DecimalField(max_digits=10, decimal_places=2)
    high_price = models.DecimalField(max_digits=10, decimal_places=2)
    low_price = models.DecimalField(max_digits=10, decimal_places=2)
    close_price = models.DecimalField(max_digits=10, decimal_places=2)
    volume = models.BigIntegerField()
    dividends = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    stock_splits = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['company', 'date']
        ordering = ['-date']
    
    def __str__(self):
        return f"{self.company.ticker_symbol} - {self.date} - Close: ${self.close_price}"
