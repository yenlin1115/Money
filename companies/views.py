from django.shortcuts import render
from django.db.models import Max
from .models import Company, StockData
import pandas as pd
import json
from decimal import Decimal
from openai_agents import TradingBoss

# Create your views here.

def stock_dashboard(request):
    companies = Company.objects.all()
    stocks_data = []
    
    for company in companies:
        # Get stock data ordered by date
        stock_data = StockData.objects.filter(company=company).order_by('date')
        
        if stock_data.exists():
            # Convert to pandas DataFrame for calculations
            df = pd.DataFrame(list(stock_data.values()))
            
            # Convert Decimal fields to float
            df['close_price'] = df['close_price'].astype(float)
            df['open_price'] = df['open_price'].astype(float)
            df['high_price'] = df['high_price'].astype(float)
            df['low_price'] = df['low_price'].astype(float)
            df['volume'] = df['volume'].astype(float)
            
            # Calculate daily returns
            df['daily_return'] = df['close_price'].pct_change() * 100
            
            # Calculate moving averages
            df['ma20'] = df['close_price'].rolling(window=20).mean()
            df['ma50'] = df['close_price'].rolling(window=50).mean()
            
            # Calculate volatility (annualized)
            volatility = df['daily_return'].std() * (252 ** 0.5)  # 252 trading days
            
            # Get latest data
            latest = stock_data.latest('date')
            previous_day = stock_data.exclude(id=latest.id).latest('date')
            daily_change = ((float(latest.close_price) - float(previous_day.close_price)) / float(previous_day.close_price)) * 100
            
            # Prepare data for charts
            dates = [d.strftime('%Y-%m-%d') for d in df['date']]
            prices = [float(p) for p in df['close_price']]
            ma20 = [float(m) if pd.notnull(m) else None for m in df['ma20']]
            ma50 = [float(m) if pd.notnull(m) else None for m in df['ma50']]
            
            stocks_data.append({
                'company': company,
                'latest_price': float(latest.close_price),
                'daily_change': daily_change,
                'latest_volume': int(latest.volume),
                'volatility': float(volatility),
                'dates': json.dumps(dates),
                'prices': json.dumps(prices),
                'ma20': json.dumps(ma20),
                'ma50': json.dumps(ma50)
            })
    
    return render(request, 'stocks.html', {'stocks': stocks_data})

def trading_predictions(request):
    companies = Company.objects.all()
    selected_stock = request.GET.get('stock', companies.first().ticker_symbol if companies.exists() else None)
    decision = None
    dates = None
    prices = None
    
    if selected_stock:
        company = Company.objects.get(ticker_symbol=selected_stock)
        stock_data = StockData.objects.filter(company=company).order_by('date')
        
        if stock_data.exists():
            # Convert to pandas DataFrame
            df = pd.DataFrame(list(stock_data.values()))
            
            # Convert Decimal fields to float
            df['close_price'] = df['close_price'].astype(float)
            df['open_price'] = df['open_price'].astype(float)
            df['high_price'] = df['high_price'].astype(float)
            df['low_price'] = df['low_price'].astype(float)
            df['volume'] = df['volume'].astype(float)
            
            # Get trading decision using OpenAI-powered agents
            boss = TradingBoss()
            decision = boss.decide(df)
            
            # Prepare data for chart
            dates = json.dumps([d.strftime('%Y-%m-%d') for d in df['date']])
            prices = json.dumps([float(p) for p in df['close_price']])
    
    return render(request, 'predictions.html', {
        'companies': companies,
        'selected_stock': selected_stock,
        'decision': decision,
        'dates': dates,
        'prices': prices
    })
