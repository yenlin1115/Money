from django.core.management.base import BaseCommand
from api.services.newsapi import NewsAPIService
from api.services.yfinance import YahooFinanceService
from companies.models import Company
from news.models import NewsArticle
from predictions.models import Prediction
from datetime import datetime, timedelta

class Command(BaseCommand):
    help = 'Fetch news and stock data for all companies'

    def handle(self, *args, **options):
        self.stdout.write('Starting data fetch...')
        
        # Initialize services
        news_service = NewsAPIService()
        stock_service = YahooFinanceService()
        
        # Get all companies
        companies = Company.objects.all()
        
        # Fetch news for each company
        for company in companies:
            self.stdout.write(f'Fetching news for {company.name}...')
            
            # Search for news
            articles = news_service.search_news(
                query=company.name,
                from_date=(datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d')
            )
            
            # Save articles
            saved_articles = news_service.save_news_articles(articles)
            self.stdout.write(f'Saved {len(saved_articles)} new articles for {company.name}')
        
        # Fetch stock data
        self.stdout.write('Fetching stock data...')
        stock_data = stock_service.get_multiple_stocks(companies)
        
        # Update predictions based on stock movements
        for company in companies:
            data = stock_data[company.ticker_symbol]
            if data['price_change'] is not None:
                # Get recent predictions
                recent_predictions = Prediction.objects.filter(
                    company=company,
                    prediction_date__gte=datetime.now() - timedelta(days=7),
                    actual_movement__isnull=True
                )
                
                for prediction in recent_predictions:
                    # Update prediction with actual movement
                    prediction.actual_movement = 'UP' if data['price_change'] > 0 else 'DOWN'
                    prediction.actual_price_change = data['price_change']
                    prediction.is_correct = (
                        (prediction.prediction == 'UP' and data['price_change'] > 0) or
                        (prediction.prediction == 'DOWN' and data['price_change'] < 0)
                    )
                    prediction.verified_at = datetime.now()
                    prediction.save()
        
        self.stdout.write(self.style.SUCCESS('Data fetch completed successfully')) 