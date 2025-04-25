import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# API Configuration
NEWSAPI_CONFIG = {
    'api_key': '2725226a0a0945a49240bd30329ffc47',  # Your NewsAPI key
    'base_url': 'https://newsapi.org/v2/',
    'endpoints': {
        'everything': 'everything',
        'top_headlines': 'top-headlines'
    }
}

GDELT_CONFIG = {
    'api_key': os.getenv('GDELT_API_KEY', 'your_gdelt_key_here'),
    'base_url': 'https://api.gdeltproject.org/api/v2/',
    'endpoints': {
        'doc': 'doc/doc',
        'timeline': 'timeline/timeline'
    }
}

YAHOO_FINANCE_CONFIG = {
    'api_key': os.getenv('YAHOO_FINANCE_API_KEY', 'your_yahoo_finance_key_here'),
    'base_url': 'https://yfapi.net/v8/',
    'endpoints': {
        'stock_data': 'finance/spark',
        'historical_data': 'finance/chart'
    }
} 