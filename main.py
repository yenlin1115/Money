import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime, timedelta
import os
import django
import sys

# Set up Django environment
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Moneytest.settings')
django.setup()

from companies.models import Company, StockData

def fetch_stock_data(ticker, start_date, end_date):
    """Fetch stock data for a given ticker and date range"""
    stock = yf.Ticker(ticker)
    data = stock.history(start=start_date, end=end_date)
    return data

def save_to_csv(data, ticker, start_date, end_date):
    """Save stock data to CSV file"""
    if not os.path.exists('data'):
        os.makedirs('data')
    
    filename = f'data/{ticker}_stock_data_{start_date.strftime("%Y%m%d")}_to_{end_date.strftime("%Y%m%d")}.csv'
    data.to_csv(filename)
    return filename

def save_to_database(data, ticker):
    """Save stock data to Django database"""
    company, created = Company.objects.get_or_create(
        ticker_symbol=ticker,
        defaults={
            'name': ticker,
            'country': 'US',
            'industry': 'Technology'
        }
    )
    
    for index, row in data.iterrows():
        StockData.objects.update_or_create(
            company=company,
            date=index.date(),
            defaults={
                'open_price': row['Open'],
                'high_price': row['High'],
                'low_price': row['Low'],
                'close_price': row['Close'],
                'volume': row['Volume'],
                'dividends': row['Dividends'],
                'stock_splits': row['Stock Splits']
            }
        )

def analyze_stock_data(data, ticker):
    """Perform basic analysis on stock data"""
    analysis = {
        'ticker': ticker,
        'start_date': data.index[0].strftime('%Y-%m-%d'),
        'end_date': data.index[-1].strftime('%Y-%m-%d'),
        'average_close': data['Close'].mean(),
        'highest_price': data['High'].max(),
        'lowest_price': data['Low'].min(),
        'total_volume': data['Volume'].sum(),
        'daily_returns': data['Close'].pct_change().dropna(),
        'volatility': data['Close'].pct_change().std() * np.sqrt(252),  # Annualized volatility
        'moving_average_20': data['Close'].rolling(window=20).mean(),
        'moving_average_50': data['Close'].rolling(window=50).mean()
    }
    return analysis

def plot_stock_data(data, ticker, analysis):
    """Create visualizations for stock data"""
    plt.style.use('seaborn-v0_8')  # Updated style name
    
    # Create figure with subplots
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10))
    
    # Price and Moving Averages
    ax1.plot(data.index, data['Close'], label='Close Price', color='blue')
    ax1.plot(data.index, analysis['moving_average_20'], label='20-day MA', color='orange')
    ax1.plot(data.index, analysis['moving_average_50'], label='50-day MA', color='red')
    ax1.set_title(f'{ticker} Stock Price and Moving Averages')
    ax1.set_ylabel('Price ($)')
    ax1.legend()
    ax1.grid(True)
    
    # Daily Returns
    ax2.hist(analysis['daily_returns'], bins=50, alpha=0.75, color='green')
    ax2.set_title(f'{ticker} Daily Returns Distribution')
    ax2.set_xlabel('Daily Returns')
    ax2.set_ylabel('Frequency')
    ax2.grid(True)
    
    # Save plot
    if not os.path.exists('plots'):
        os.makedirs('plots')
    plt.savefig(f'plots/{ticker}_analysis.png')
    plt.close()

def main():
    # Define stocks and date range
    stocks = ['TSLA', 'AAPL']
    end_date = datetime.now()
    start_date = end_date - timedelta(days=180)
    
    print(f"Fetching stock data from {start_date.strftime('%Y-%m-%d')} to {end_date.strftime('%Y-%m-%d')}")
    
    for ticker in stocks:
        print(f"\nProcessing {ticker}...")
        
        # Fetch data
        data = fetch_stock_data(ticker, start_date, end_date)
        
        # Save to CSV
        csv_file = save_to_csv(data, ticker, start_date, end_date)
        print(f"Data saved to {csv_file}")
        
        # Save to database
        save_to_database(data, ticker)
        print("Data saved to database")
        
        # Analyze data
        analysis = analyze_stock_data(data, ticker)
        print("\nAnalysis Results:")
        print(f"Average Closing Price: ${analysis['average_close']:.2f}")
        print(f"Highest Price: ${analysis['highest_price']:.2f}")
        print(f"Lowest Price: ${analysis['lowest_price']:.2f}")
        print(f"Total Trading Volume: {analysis['total_volume']:,.0f}")
        print(f"Annualized Volatility: {analysis['volatility']:.2%}")
        
        # Create visualizations
        plot_stock_data(data, ticker, analysis)
        print(f"Visualizations saved to plots/{ticker}_analysis.png")

if __name__ == "__main__":
    main()
