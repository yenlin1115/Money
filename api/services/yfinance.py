import yfinance as yf
from typing import Dict, Any, List
from datetime import datetime, timedelta
from companies.models import Company

class YahooFinanceService:
    def __init__(self):
        self.ticker_cache = {}

    def get_stock_data(self, company: Company, days: int = 5) -> Dict[str, Any]:
        """
        Get stock data for a company
        """
        if company.ticker_symbol not in self.ticker_cache:
            self.ticker_cache[company.ticker_symbol] = yf.Ticker(company.ticker_symbol)

        ticker = self.ticker_cache[company.ticker_symbol]
        
        # Get historical data
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)
        
        hist = ticker.history(start=start_date, end=end_date)
        
        if hist.empty:
            return {
                'current_price': None,
                'price_change': None,
                'price_change_percent': None,
                'historical_data': []
            }

        # Calculate price changes
        current_price = hist['Close'].iloc[-1]
        previous_price = hist['Close'].iloc[0]
        price_change = current_price - previous_price
        price_change_percent = (price_change / previous_price) * 100

        # Format historical data
        historical_data = []
        for date, row in hist.iterrows():
            historical_data.append({
                'date': date.strftime('%Y-%m-%d'),
                'open': row['Open'],
                'high': row['High'],
                'low': row['Low'],
                'close': row['Close'],
                'volume': row['Volume']
            })

        return {
            'current_price': current_price,
            'price_change': price_change,
            'price_change_percent': price_change_percent,
            'historical_data': historical_data
        }

    def get_multiple_stocks(self, companies: List[Company], days: int = 5) -> Dict[str, Dict[str, Any]]:
        """
        Get stock data for multiple companies
        """
        results = {}
        for company in companies:
            results[company.ticker_symbol] = self.get_stock_data(company, days)
        return results 