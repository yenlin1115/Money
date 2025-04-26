import openai
from typing import Dict, Any, List
import pandas as pd
from datetime import datetime
import json
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Initialize OpenAI client with API key
openai.api_key = os.getenv('OPENAI_API_KEY')

class BaseTradingAgent:
    def __init__(self, name: str):
        self.name = name
    
    def analyze(self, data: pd.DataFrame) -> Dict[str, Any]:
        """Basic technical analysis fallback"""
        # Calculate basic indicators
        close_prices = data['close_price']
        ma20 = close_prices.rolling(window=20).mean()
        ma50 = close_prices.rolling(window=50).mean()
        daily_returns = close_prices.pct_change()
        volatility = daily_returns.rolling(window=20).std()
        
        # Get latest values
        latest_price = close_prices.iloc[-1]
        latest_ma20 = ma20.iloc[-1]
        latest_ma50 = ma50.iloc[-1]
        latest_volatility = volatility.iloc[-1]
        
        # Basic trading rules
        if latest_price > latest_ma20 and latest_price > latest_ma50:
            action = "BUY"
            confidence = 0.7
        elif latest_price < latest_ma20 and latest_price < latest_ma50:
            action = "SELL"
            confidence = 0.7
        else:
            action = "HOLD"
            confidence = 0.5
        
        # Calculate risk level based on volatility
        risk_level = min(latest_volatility * 10, 1.0)  # Normalize to 0-1 range
        
        # Estimate expected return based on recent trend
        recent_trend = (latest_price - close_prices.iloc[-5]) / close_prices.iloc[-5]
        expected_return = recent_trend * 100  # Convert to percentage
        
        return {
            "action": action,
            "confidence": confidence,
            "risk_level": risk_level,
            "expected_return": expected_return,
            "reasoning": f"Basic technical analysis: Price {latest_price:.2f}, MA20 {latest_ma20:.2f}, MA50 {latest_ma50:.2f}"
        }

class OpenAITradingAgent(BaseTradingAgent):
    def __init__(self, name: str, role: str, model: str = "gpt-4-turbo-preview"):
        super().__init__(name)
        self.role = role
        self.model = model
        self.client = openai.OpenAI(api_key=openai.api_key)
    
    def analyze(self, data: pd.DataFrame) -> Dict[str, Any]:
        """Analyze stock data using OpenAI and return trading recommendation"""
        # If no API key is available, fall back to basic analysis
        if not openai.api_key:
            return super().analyze(data)
        
        # Prepare data summary for the agent
        data_summary = self._prepare_data_summary(data)
        
        # Create the system message
        system_message = f"""You are a {self.role} trading agent. Your task is to analyze stock data and provide a trading recommendation.
        Consider the following in your analysis:
        - Price trends and patterns
        - Technical indicators
        - Market conditions
        - Risk factors
        
        Provide your recommendation in the following format:
        {{
            "action": "BUY", "SELL", or "HOLD",
            "confidence": float between 0 and 1,
            "risk_level": float between 0 and 1,
            "expected_return": float percentage,
            "reasoning": "detailed explanation"
        }}
        """
        
        # Create the user message
        user_message = f"""Please analyze the following stock data and provide a trading recommendation:
        
        {data_summary}
        """
        
        try:
            # Call OpenAI API
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_message},
                    {"role": "user", "content": user_message}
                ],
                response_format={"type": "json_object"}
            )
            
            # Parse the response
            recommendation = json.loads(response.choices[0].message.content)
            return recommendation
            
        except Exception as e:
            print(f"Error in {self.name}: {str(e)}")
            return super().analyze(data)
    
    def _prepare_data_summary(self, data: pd.DataFrame) -> str:
        """Prepare a summary of the stock data for the agent"""
        latest = data.iloc[-1]
        previous = data.iloc[-2]
        
        summary = f"""
        Latest Data:
        - Date: {latest.name}
        - Close Price: ${latest['close_price']:.2f}
        - Volume: {latest['volume']:,.0f}
        - Daily Change: {((latest['close_price'] - previous['close_price']) / previous['close_price'] * 100):.2f}%
        
        Recent Trends:
        - 20-day Moving Average: ${data['close_price'].rolling(window=20).mean().iloc[-1]:.2f}
        - 50-day Moving Average: ${data['close_price'].rolling(window=50).mean().iloc[-1]:.2f}
        - Volatility (20-day): {data['close_price'].pct_change().rolling(window=20).std().iloc[-1] * 100:.2f}%
        
        Price Range (Last 20 days):
        - High: ${data['high_price'].iloc[-20:].max():.2f}
        - Low: ${data['low_price'].iloc[-20:].min():.2f}
        """
        return summary

class TechnicalAgent(OpenAITradingAgent):
    def __init__(self):
        super().__init__(
            name="Technical Analyst",
            role="technical analysis expert specializing in price patterns, trends, and technical indicators"
        )

class FundamentalAgent(OpenAITradingAgent):
    def __init__(self):
        super().__init__(
            name="Fundamental Analyst",
            role="fundamental analysis expert specializing in company financials and market valuation"
        )

class SentimentAgent(OpenAITradingAgent):
    def __init__(self):
        super().__init__(
            name="Sentiment Analyst",
            role="market sentiment analysis expert specializing in investor psychology and market mood"
        )

class NewsAgent(OpenAITradingAgent):
    def __init__(self):
        super().__init__(
            name="News Analyst",
            role="news analysis expert specializing in market-moving events and their impact"
        )

class TradingBoss:
    def __init__(self):
        self.agents = [
            TechnicalAgent(),
            FundamentalAgent(),
            SentimentAgent(),
            NewsAgent()
        ]
    
    def decide(self, data: pd.DataFrame) -> Dict[str, Any]:
        """Make final trading decision based on all agents' recommendations"""
        recommendations = {}
        
        # Get recommendations from all agents
        for agent in self.agents:
            recommendations[agent.name] = agent.analyze(data)
        
        # If no API key is available, use basic decision making
        if not openai.api_key:
            return self._make_basic_decision(recommendations)
        
        # Create the system message for the boss
        system_message = """You are a trading boss that makes final trading decisions based on multiple expert recommendations.
        Consider the following in your decision:
        - Each agent's recommendation and confidence
        - Risk levels
        - Expected returns
        - Overall market conditions
        
        Provide your final decision in the following format:
        {
            "final_action": "BUY", "SELL", or "HOLD",
            "confidence": float between 0 and 1,
            "risk_level": float between 0 and 1,
            "expected_return": float percentage,
            "chosen_agent": "name of the most influential agent",
            "all_recommendations": {original recommendations},
            "reasoning": "detailed explanation of the final decision"
        }
        """
        
        # Create the user message
        user_message = f"""Please make a final trading decision based on these expert recommendations:
        
        {json.dumps(recommendations, indent=2)}
        """
        
        try:
            # Call OpenAI API for the final decision
            response = openai.OpenAI(api_key=openai.api_key).chat.completions.create(
                model="gpt-4-turbo-preview",
                messages=[
                    {"role": "system", "content": system_message},
                    {"role": "user", "content": user_message}
                ],
                response_format={"type": "json_object"}
            )
            
            # Parse the response
            final_decision = json.loads(response.choices[0].message.content)
            return final_decision
            
        except Exception as e:
            print(f"Error in TradingBoss: {str(e)}")
            return self._make_basic_decision(recommendations)
    
    def _make_basic_decision(self, recommendations: Dict[str, Any]) -> Dict[str, Any]:
        """Make a basic decision when no API key is available"""
        # Count the votes for each action
        action_counts = {"BUY": 0, "SELL": 0, "HOLD": 0}
        total_confidence = 0
        total_risk = 0
        total_return = 0
        
        for rec in recommendations.values():
            action_counts[rec["action"]] += 1
            total_confidence += rec["confidence"]
            total_risk += rec["risk_level"]
            total_return += rec["expected_return"]
        
        # Determine final action based on majority vote
        final_action = max(action_counts.items(), key=lambda x: x[1])[0]
        
        # Calculate averages
        num_agents = len(recommendations)
        avg_confidence = total_confidence / num_agents
        avg_risk = total_risk / num_agents
        avg_return = total_return / num_agents
        
        # Find the most confident agent
        chosen_agent = max(recommendations.items(), key=lambda x: x[1]["confidence"])[0]
        
        return {
            "final_action": final_action,
            "confidence": avg_confidence,
            "risk_level": avg_risk,
            "expected_return": avg_return,
            "chosen_agent": chosen_agent,
            "all_recommendations": recommendations,
            "reasoning": f"Basic decision based on majority vote: {action_counts}"
        } 