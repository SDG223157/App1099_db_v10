import requests
import logging
from typing import Dict
import json

class NewsAnalyzer:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://api.deepseek.com"
        self.headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        self.logger = logging.getLogger(__name__)

    def analyze_sentiment(self, text: str) -> Dict:
        try:
            endpoint = f"{self.base_url}/sentiment"
            payload = {"text": text}
            
            response = requests.post(
                endpoint,
                headers=self.headers,
                json=payload
            )
            response.raise_for_status()
            result = response.json()
            
            sentiment_map = {
                0: "NEGATIVE",
                1: "NEUTRAL",
                2: "POSITIVE"
            }
            
            sentiment = sentiment_map[result['sentiment']]
            confidence = result['confidence']
            
            strength = "Strong" if confidence > 0.8 else "Moderate" if confidence > 0.6 else "Weak"
            explanation = f"{strength} {sentiment.lower()} sentiment detected"
            
            return {
                "overall_sentiment": sentiment,
                "explanation": explanation,
                "confidence": confidence,
                "scores": result['scores']
            }
            
        except Exception as e:
            self.logger.error(f"Error in sentiment analysis: {str(e)}")
            return {"overall_sentiment": "NEUTRAL", "confidence": 0}

    def generate_summary(self, text: str) -> Dict:
        try:
            endpoint = f"{self.base_url}/summarize"
            
            # Generate brief summary
            brief_payload = {
                "text": text,
                "max_length": 128,
                "style": "brief"
            }
            brief_response = requests.post(
                endpoint,
                headers=self.headers,
                json=brief_payload
            )
            brief_response.raise_for_status()
            
            # Generate key points
            points_payload = {
                "text": text,
                "max_length": 256,
                "style": "bullet_points",
                "num_sequences": 3
            }
            points_response = requests.post(
                endpoint,
                headers=self.headers,
                json=points_payload
            )
            points_response.raise_for_status()
            
            # Generate market impact
            market_payload = {
                "text": f"Summarize the market impact: {text}",
                "max_length": 128,
                "style": "analytical"
            }
            market_response = requests.post(
                endpoint,
                headers=self.headers,
                json=market_payload
            )
            market_response.raise_for_status()
            
            return {
                "brief": brief_response.json()['summary'],
                "key_points": " ".join(points_response.json()['summaries']),
                "market_impact": market_response.json()['summary']
            }
            
        except Exception as e:
            self.logger.error(f"Error generating summary: {str(e)}")
            return {"brief": "Summary unavailable", "key_points": ""}
        
        
import os
# from news_analyzer import NewsAnalyzer
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)

def test_news_analyzer():
    # Initialize with your API key
    api_key = os.getenv("sk-32b3417ccbd047028fa01e5a433aa158")
    analyzer = NewsAnalyzer(api_key)
    
    # Test article
    test_article = """
    Tesla (TSLA) shares surged 15% today after reporting strong Q4 earnings, 
    beating analyst expectations. The electric vehicle maker reported revenue 
    of $25.1 billion, up 37% year-over-year, and earnings per share of $1.75. 
    The company also announced plans to accelerate production of its Cybertruck 
    and expects to deliver 2 million vehicles in 2024, a 50% increase from 2023.
    """
    
    # Test sentiment analysis
    print("\n=== Testing Sentiment Analysis ===")
    sentiment_result = analyzer.analyze_sentiment(test_article)
    print(f"Sentiment: {sentiment_result['overall_sentiment']}")
    print(f"Confidence: {sentiment_result['confidence']:.2f}")
    # print(f"Explanation: {sentiment_result['explanation']}")
    
    # Test summary generation
    print("\n=== Testing Summary Generation ===")
    summary_result = analyzer.generate_summary(test_article)
    print("\nBrief Summary:")
    print(summary_result['brief'])
    print("\nKey Points:")
    print(summary_result['key_points'])
    print("\nMarket Impact:")
    # print(summary_result['market_impact'])

if __name__ == "__main__":
    test_news_analyzer()