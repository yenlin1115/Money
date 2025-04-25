from typing import List, Dict, Any
from .base import BaseAPIService
from api.config import NEWSAPI_CONFIG
from news.models import NewsArticle
from companies.models import Company

class NewsAPIService(BaseAPIService):
    def __init__(self):
        super().__init__(NEWSAPI_CONFIG)
        self.session.headers.update({
            'X-Api-Key': self.config['api_key']
        })

    def search_news(self, query: str, from_date: str = None, to_date: str = None) -> List[Dict[str, Any]]:
        """
        Search for news articles related to tariffs and trade
        """
        params = {
            'q': f"{query} AND (tariff OR trade war)",
            'language': 'en',
            'sortBy': 'publishedAt',
            'pageSize': 100
        }
        
        if from_date:
            params['from'] = from_date
        if to_date:
            params['to'] = to_date

        response = self._make_request(self.config['endpoints']['everything'], params)
        return response.get('articles', [])

    def save_news_articles(self, articles: List[Dict[str, Any]]) -> List[NewsArticle]:
        """
        Save news articles to the database
        """
        saved_articles = []
        for article in articles:
            # Check if article already exists
            if NewsArticle.objects.filter(url=article['url']).exists():
                continue

            # Create new article
            news_article = NewsArticle(
                title=article['title'],
                content=article.get('description', '') + '\n' + article.get('content', ''),
                source='NEWSAPI',
                url=article['url'],
                published_date=article['publishedAt']
            )
            news_article.save()
            saved_articles.append(news_article)
        return saved_articles 