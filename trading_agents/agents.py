import numpy as np
import pandas as pd
from datetime import datetime, timedelta
from typing import Dict, List, Any
import json

class BaseAgent:
    def __init__(self, name: str):
        self.name = name
        self.past_recommendations = []
        self.past_performance = []
    
    def calculate_confidence_score(self, data: pd.DataFrame) -> float:
        """Calculate a confidence score between 0 and 1"""
        raise NotImplementedError
    
    def calculate_risk_level(self, data: pd.DataFrame) -> float:
        """Calculate risk level between 0 and 1"""
        raise NotImplementedError
    
    def calculate_expected_return(self, data: pd.DataFrame) -> float:
        """Calculate expected return as a percentage"""
        raise NotImplementedError
    
    def generate_recommendation(self, stock_data: pd.DataFrame) -> Dict[str, Any]:
        """Generate a trading recommendation"""
        raise NotImplementedError

class SwingTradingAgent(BaseAgent):
    def __init__(self):
        super().__init__("Swing Trading Agent")
        self.lookback_period = 14  # days
        self.support_resistance_window = 5
    
    def calculate_confidence_score(self, data: pd.DataFrame) -> float:
        # Calculate confidence based on trend strength and volume
        price_std = data['close_price'].std()
        volume_std = data['volume'].std()
        return min(1.0, (price_std + volume_std) / 2)
    
    def calculate_risk_level(self, data: pd.DataFrame) -> float:
        # Calculate risk based on volatility and recent price movements
        volatility = data['close_price'].pct_change().std()
        return min(1.0, volatility * 10)
    
    def calculate_expected_return(self, data: pd.DataFrame) -> float:
        # Calculate expected return based on recent price movements
        recent_returns = data['close_price'].pct_change().tail(self.lookback_period)
        return recent_returns.mean() * 100
    
    def generate_recommendation(self, stock_data: pd.DataFrame) -> Dict[str, Any]:
        data = stock_data.copy()
        data['returns'] = data['close_price'].pct_change()
        
        # Calculate support and resistance levels
        data['support'] = data['low_price'].rolling(window=self.support_resistance_window).min()
        data['resistance'] = data['high_price'].rolling(window=self.support_resistance_window).max()
        
        current_price = data['close_price'].iloc[-1]
        support = data['support'].iloc[-1]
        resistance = data['resistance'].iloc[-1]
        
        # Generate recommendation
        if current_price < support:
            action = "BUY"
            confidence = self.calculate_confidence_score(data)
            risk = self.calculate_risk_level(data)
            expected_return = self.calculate_expected_return(data)
        elif current_price > resistance:
            action = "SELL"
            confidence = self.calculate_confidence_score(data)
            risk = self.calculate_risk_level(data)
            expected_return = -self.calculate_expected_return(data)
        else:
            action = "HOLD"
            confidence = 0.5
            risk = 0.5
            expected_return = 0
        
        return {
            "agent": self.name,
            "action": action,
            "confidence": confidence,
            "risk_level": risk,
            "expected_return": expected_return,
            "timestamp": datetime.now().isoformat()
        }

class MomentumTradingAgent(BaseAgent):
    def __init__(self):
        super().__init__("Momentum Trading Agent")
        self.short_window = 10
        self.long_window = 30
    
    def calculate_confidence_score(self, data: pd.DataFrame) -> float:
        # Calculate confidence based on momentum strength
        short_ma = data['close_price'].rolling(window=self.short_window).mean()
        long_ma = data['close_price'].rolling(window=self.long_window).mean()
        momentum = (short_ma - long_ma) / long_ma
        return min(1.0, abs(momentum.iloc[-1]))
    
    def calculate_risk_level(self, data: pd.DataFrame) -> float:
        # Calculate risk based on momentum volatility
        returns = data['close_price'].pct_change()
        momentum_volatility = returns.rolling(window=self.short_window).std()
        return min(1.0, momentum_volatility.iloc[-1] * 10)
    
    def calculate_expected_return(self, data: pd.DataFrame) -> float:
        # Calculate expected return based on momentum
        short_ma = data['close_price'].rolling(window=self.short_window).mean()
        long_ma = data['close_price'].rolling(window=self.long_window).mean()
        momentum = (short_ma - long_ma) / long_ma
        return momentum.iloc[-1] * 100
    
    def generate_recommendation(self, stock_data: pd.DataFrame) -> Dict[str, Any]:
        data = stock_data.copy()
        
        # Calculate moving averages
        short_ma = data['close_price'].rolling(window=self.short_window).mean()
        long_ma = data['close_price'].rolling(window=self.long_window).mean()
        
        # Generate recommendation
        if short_ma.iloc[-1] > long_ma.iloc[-1]:
            action = "BUY"
        else:
            action = "SELL"
        
        confidence = self.calculate_confidence_score(data)
        risk = self.calculate_risk_level(data)
        expected_return = self.calculate_expected_return(data)
        
        return {
            "agent": self.name,
            "action": action,
            "confidence": confidence,
            "risk_level": risk,
            "expected_return": expected_return,
            "timestamp": datetime.now().isoformat()
        }

class ValueInvestingAgent(BaseAgent):
    def __init__(self):
        super().__init__("Value Investing Agent")
        self.valuation_window = 90  # days
    
    def calculate_confidence_score(self, data: pd.DataFrame) -> float:
        # Calculate confidence based on valuation metrics
        price_to_ma = data['close_price'].iloc[-1] / data['close_price'].rolling(window=self.valuation_window).mean().iloc[-1]
        return min(1.0, abs(1 - price_to_ma))
    
    def calculate_risk_level(self, data: pd.DataFrame) -> float:
        # Calculate risk based on price volatility and valuation
        volatility = data['close_price'].pct_change().std()
        price_to_ma = data['close_price'].iloc[-1] / data['close_price'].rolling(window=self.valuation_window).mean().iloc[-1]
        return min(1.0, (volatility + abs(1 - price_to_ma)) / 2)
    
    def calculate_expected_return(self, data: pd.DataFrame) -> float:
        # Calculate expected return based on mean reversion
        ma = data['close_price'].rolling(window=self.valuation_window).mean().iloc[-1]
        current_price = data['close_price'].iloc[-1]
        return ((ma - current_price) / current_price) * 100
    
    def generate_recommendation(self, stock_data: pd.DataFrame) -> Dict[str, Any]:
        data = stock_data.copy()
        
        # Calculate valuation metrics
        ma = data['close_price'].rolling(window=self.valuation_window).mean().iloc[-1]
        current_price = data['close_price'].iloc[-1]
        
        # Generate recommendation
        if current_price < ma * 0.95:  # 5% below moving average
            action = "BUY"
        elif current_price > ma * 1.05:  # 5% above moving average
            action = "SELL"
        else:
            action = "HOLD"
        
        confidence = self.calculate_confidence_score(data)
        risk = self.calculate_risk_level(data)
        expected_return = self.calculate_expected_return(data)
        
        return {
            "agent": self.name,
            "action": action,
            "confidence": confidence,
            "risk_level": risk,
            "expected_return": expected_return,
            "timestamp": datetime.now().isoformat()
        }

class QuantitativeTradingAgent(BaseAgent):
    def __init__(self):
        super().__init__("Quantitative Trading Agent")
        self.feature_window = 20
        self.prediction_window = 5
    
    def calculate_confidence_score(self, data: pd.DataFrame) -> float:
        # Calculate confidence based on model prediction strength
        returns = data['close_price'].pct_change()
        volatility = returns.rolling(window=self.feature_window).std()
        return min(1.0, 1 - volatility.iloc[-1])
    
    def calculate_risk_level(self, data: pd.DataFrame) -> float:
        # Calculate risk based on prediction uncertainty
        returns = data['close_price'].pct_change()
        volatility = returns.rolling(window=self.feature_window).std()
        return min(1.0, volatility.iloc[-1] * 10)
    
    def calculate_expected_return(self, data: pd.DataFrame) -> float:
        # Calculate expected return based on statistical model
        returns = data['close_price'].pct_change()
        expected_return = returns.rolling(window=self.feature_window).mean().iloc[-1]
        return expected_return * 100
    
    def generate_recommendation(self, stock_data: pd.DataFrame) -> Dict[str, Any]:
        data = stock_data.copy()
        
        # Calculate technical indicators
        returns = data['close_price'].pct_change()
        volatility = returns.rolling(window=self.feature_window).std()
        momentum = returns.rolling(window=self.feature_window).mean()
        
        # Generate recommendation based on statistical model
        if momentum.iloc[-1] > 0 and volatility.iloc[-1] < 0.02:
            action = "BUY"
        elif momentum.iloc[-1] < 0 and volatility.iloc[-1] < 0.02:
            action = "SELL"
        else:
            action = "HOLD"
        
        confidence = self.calculate_confidence_score(data)
        risk = self.calculate_risk_level(data)
        expected_return = self.calculate_expected_return(data)
        
        return {
            "agent": self.name,
            "action": action,
            "confidence": confidence,
            "risk_level": risk,
            "expected_return": expected_return,
            "timestamp": datetime.now().isoformat()
        }

class TradingBoss:
    def __init__(self):
        self.agents = {
            "swing": SwingTradingAgent(),
            "momentum": MomentumTradingAgent(),
            "value": ValueInvestingAgent(),
            "quant": QuantitativeTradingAgent()
        }
        self.past_decisions = []
        self.agent_weights = {
            "swing": 0.25,
            "momentum": 0.25,
            "value": 0.25,
            "quant": 0.25
        }
    
    def evaluate_recommendation(self, recommendation: Dict[str, Any]) -> float:
        """Evaluate a single recommendation and return a score"""
        # Higher confidence and expected return, lower risk is better
        score = (
            recommendation["confidence"] * 0.4 +
            (recommendation["expected_return"] / 100) * 0.4 +
            (1 - recommendation["risk_level"]) * 0.2
        )
        return score
    
    def decide(self, stock_data: pd.DataFrame) -> Dict[str, Any]:
        """Make final trading decision based on all agents' recommendations"""
        recommendations = {}
        scores = {}
        
        # Get recommendations from all agents
        for agent_name, agent in self.agents.items():
            recommendation = agent.generate_recommendation(stock_data)
            recommendations[agent_name] = recommendation
            scores[agent_name] = self.evaluate_recommendation(recommendation)
        
        # Calculate weighted scores
        weighted_scores = {
            agent: score * self.agent_weights[agent]
            for agent, score in scores.items()
        }
        
        # Find best recommendation
        best_agent = max(weighted_scores, key=weighted_scores.get)
        best_recommendation = recommendations[best_agent]
        
        # Record decision
        decision = {
            "final_action": best_recommendation["action"],
            "confidence": best_recommendation["confidence"],
            "risk_level": best_recommendation["risk_level"],
            "expected_return": best_recommendation["expected_return"],
            "chosen_agent": best_agent,
            "all_recommendations": recommendations,
            "timestamp": datetime.now().isoformat()
        }
        
        self.past_decisions.append(decision)
        return decision
    
    def update_weights(self, performance_data: Dict[str, float]):
        """Update agent weights based on past performance"""
        total_performance = sum(performance_data.values())
        if total_performance > 0:
            self.agent_weights = {
                agent: performance / total_performance
                for agent, performance in performance_data.items()
            } 