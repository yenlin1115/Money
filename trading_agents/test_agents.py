import pandas as pd
from agents import TradingBoss
from datetime import datetime, timedelta
import random

def generate_sample_data(days: int = 100) -> pd.DataFrame:
    """Generate sample stock data for testing"""
    dates = pd.date_range(end=datetime.now(), periods=days)
    base_price = 100.0
    prices = []
    
    for i in range(days):
        if i == 0:
            price = base_price
        else:
            # Generate random price movement
            change = random.uniform(-2.0, 2.0)
            price = prices[-1] * (1 + change/100)
        prices.append(price)
    
    data = pd.DataFrame({
        'date': dates,
        'open_price': [p * random.uniform(0.99, 1.01) for p in prices],
        'high_price': [p * random.uniform(1.01, 1.03) for p in prices],
        'low_price': [p * random.uniform(0.97, 0.99) for p in prices],
        'close_price': prices,
        'volume': [random.randint(1000000, 5000000) for _ in range(days)]
    })
    
    return data

def main():
    # Create trading boss
    boss = TradingBoss()
    
    # Generate sample data
    stock_data = generate_sample_data()
    
    # Get trading decision
    decision = boss.decide(stock_data)
    
    # Print results
    print("\n=== Trading Decision ===")
    print(f"Final Action: {decision['final_action']}")
    print(f"Confidence: {decision['confidence']:.2f}")
    print(f"Risk Level: {decision['risk_level']:.2f}")
    print(f"Expected Return: {decision['expected_return']:.2f}%")
    print(f"Chosen Agent: {decision['chosen_agent']}")
    
    print("\n=== Individual Agent Recommendations ===")
    for agent, rec in decision['all_recommendations'].items():
        print(f"\n{rec['agent']}:")
        print(f"  Action: {rec['action']}")
        print(f"  Confidence: {rec['confidence']:.2f}")
        print(f"  Risk Level: {rec['risk_level']:.2f}")
        print(f"  Expected Return: {rec['expected_return']:.2f}%")

if __name__ == "__main__":
    main() 