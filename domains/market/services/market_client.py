import sys
import random
import json
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
from pathlib import Path

# 상위 디렉토리 추가
ROOT_DIR = Path(__file__).parent.parent.parent.parent
sys.path.append(str(ROOT_DIR))

from shared.services.base_client import BaseApiClient
from shared.models.common_models import MarketData, AnalysisResult

class MarketClient(BaseApiClient):
    """시장 분석 데이터 API 클라이언트"""
    
    def __init__(self, base_url: str, api_key: str = "", ws_url: str = ""):
        """
        MarketClient 초기화
        
        Args:
            base_url: API 기본 URL
            api_key: API 키
            ws_url: WebSocket URL
        """
        super().__init__(base_url, api_key, ws_url)
    
    def get_market_overview(self) -> Dict[str, Any]:
        """
        전체 암호화폐 시장 개요를 가져옵니다.
        
        Returns:
            Dict[str, Any]: 시장 개요 데이터
        """
        try:
            # 실제 API 호출 대신 데모 데이터 생성
            now = datetime.now()
            yesterday = now - timedelta(days=1)
            
            # 시장 개요 데이터
            total_market_cap = 2.1e12 + random.uniform(-1e11, 1e11)
            market_cap_change = random.uniform(-0.05, 0.05)
            total_volume_24h = 1.2e11 + random.uniform(-1e10, 1e10)
            volume_change_24h = random.uniform(-0.1, 0.1)
            btc_dominance = 45 + random.uniform(-2, 2)
            eth_dominance = 18 + random.uniform(-1, 1)
            
            return {
                "total_market_cap": total_market_cap,
                "market_cap_change_24h": market_cap_change,
                "total_volume_24h": total_volume_24h,
                "volume_change_24h": volume_change_24h,
                "btc_dominance": btc_dominance,
                "eth_dominance": eth_dominance,
                "active_cryptocurrencies": 10000 + random.randint(-500, 500),
                "active_exchanges": 500 + random.randint(-20, 20),
                "updated_at": now.isoformat()
            }
        except Exception as e:
            self.logger.error(f"시장 개요 가져오기 실패: {str(e)}")
            return {"error": str(e)}
    
    def get_top_coins(self, limit: int = 10, sort_by: str = "market_cap") -> List[Dict[str, Any]]:
        """
        시가총액 기준 상위 코인 목록을 가져옵니다.
        
        Args:
            limit: 최대 결과 수
            sort_by: 정렬 기준 (market_cap, volume, change_24h)
            
        Returns:
            List[Dict[str, Any]]: 상위 코인 목록
        """
        try:
            # 기본 코인 데이터
            coins = [
                {"symbol": "BTC", "name": "Bitcoin", "market_cap": 1e12, "price": 50000, "volume_24h": 3e10, "change_24h": 0.02},
                {"symbol": "ETH", "name": "Ethereum", "market_cap": 4e11, "price": 3000, "volume_24h": 2e10, "change_24h": 0.03},
                {"symbol": "BNB", "name": "Binance Coin", "market_cap": 8e10, "price": 500, "volume_24h": 2e9, "change_24h": -0.01},
                {"symbol": "SOL", "name": "Solana", "market_cap": 4e10, "price": 100, "volume_24h": 3e9, "change_24h": 0.05},
                {"symbol": "XRP", "name": "Ripple", "market_cap": 3e10, "price": 0.5, "volume_24h": 2e9, "change_24h": -0.02},
                {"symbol": "ADA", "name": "Cardano", "market_cap": 2e10, "price": 0.6, "volume_24h": 1e9, "change_24h": 0.01},
                {"symbol": "DOGE", "name": "Dogecoin", "market_cap": 1.5e10, "price": 0.1, "volume_24h": 1e9, "change_24h": 0.04},
                {"symbol": "DOT", "name": "Polkadot", "market_cap": 1e10, "price": 8, "volume_24h": 8e8, "change_24h": -0.01},
                {"symbol": "AVAX", "name": "Avalanche", "market_cap": 9e9, "price": 30, "volume_24h": 7e8, "change_24h": 0.02},
                {"symbol": "LINK", "name": "Chainlink", "market_cap": 8e9, "price": 15, "volume_24h": 6e8, "change_24h": 0.03},
                {"symbol": "MATIC", "name": "Polygon", "market_cap": 7e9, "price": 0.8, "volume_24h": 5e8, "change_24h": -0.01},
                {"symbol": "UNI", "name": "Uniswap", "market_cap": 6e9, "price": 7, "volume_24h": 4e8, "change_24h": 0.02},
                {"symbol": "ATOM", "name": "Cosmos", "market_cap": 5e9, "price": 12, "volume_24h": 3e8, "change_24h": 0.04},
                {"symbol": "ALGO", "name": "Algorand", "market_cap": 4e9, "price": 0.3, "volume_24h": 2e8, "change_24h": -0.02},
                {"symbol": "XLM", "name": "Stellar", "market_cap": 3e9, "price": 0.1, "volume_24h": 1e8, "change_24h": 0.01}
            ]
            
            # 약간의 랜덤성 추가
            for coin in coins:
                market_cap_change = random.uniform(-0.05, 0.05)
                price_change = random.uniform(-0.05, 0.05)
                volume_change = random.uniform(-0.1, 0.1)
                change_24h_delta = random.uniform(-0.02, 0.02)
                
                coin["market_cap"] *= (1 + market_cap_change)
                coin["price"] *= (1 + price_change)
                coin["volume_24h"] *= (1 + volume_change)
                coin["change_24h"] += change_24h_delta
            
            # 정렬
            if sort_by == "market_cap":
                coins.sort(key=lambda x: x["market_cap"], reverse=True)
            elif sort_by == "volume":
                coins.sort(key=lambda x: x["volume_24h"], reverse=True)
            elif sort_by == "change_24h":
                coins.sort(key=lambda x: x["change_24h"], reverse=True)
            
            # 시간 추가
            for coin in coins:
                coin["updated_at"] = datetime.now().isoformat()
            
            return coins[:limit]
        except Exception as e:
            self.logger.error(f"상위 코인 목록 가져오기 실패: {str(e)}")
            return []
    
    def get_market_cap_distribution(self) -> Dict[str, Any]:
        """
        시가총액 분포를 가져옵니다.
        
        Returns:
            Dict[str, Any]: 시가총액 분포 데이터
        """
        try:
            # 시가총액 분포 데이터
            categories = [
                {"name": "Large Cap (>$10B)", "value": 75},
                {"name": "Mid Cap ($1B-$10B)", "value": 15},
                {"name": "Small Cap ($100M-$1B)", "value": 7},
                {"name": "Micro Cap (<$100M)", "value": 3}
            ]
            
            # 랜덤 변동 추가
            total = 100
            for i in range(len(categories) - 1):
                delta = random.uniform(-2, 2)
                if categories[i]["value"] + delta > 0:
                    categories[i]["value"] += delta
                    total -= delta
            
            categories[-1]["value"] = total
            
            return {
                "categories": categories,
                "updated_at": datetime.now().isoformat()
            }
        except Exception as e:
            self.logger.error(f"시가총액 분포 가져오기 실패: {str(e)}")
            return {"error": str(e)}
    
    def get_market_sentiment(self) -> Dict[str, Any]:
        """
        시장 감정 지표를 가져옵니다.
        
        Returns:
            Dict[str, Any]: 시장 감정 데이터
        """
        try:
            # 감정 지표 데이터 생성
            fear_greed_index = random.randint(20, 80)
            
            # 지표 범위에 따른 상태 결정
            if fear_greed_index < 25:
                sentiment = "Extreme Fear"
            elif fear_greed_index < 45:
                sentiment = "Fear"
            elif fear_greed_index < 55:
                sentiment = "Neutral"
            elif fear_greed_index < 75:
                sentiment = "Greed"
            else:
                sentiment = "Extreme Greed"
            
            # 과거 7일 데이터 생성
            now = datetime.now()
            historical = []
            
            for i in range(7):
                day = now - timedelta(days=i)
                historical.append({
                    "date": day.strftime("%Y-%m-%d"),
                    "value": random.randint(20, 80)
                })
            
            return {
                "fear_greed_index": fear_greed_index,
                "sentiment": sentiment,
                "historical": historical,
                "updated_at": now.isoformat()
            }
        except Exception as e:
            self.logger.error(f"시장 감정 지표 가져오기 실패: {str(e)}")
            return {"error": str(e)}
    
    def get_market_trends(self, period: str = "1w") -> Dict[str, Any]:
        """
        시장 트렌드 데이터를 가져옵니다.
        
        Args:
            period: 기간 (1d, 1w, 1m, 3m)
            
        Returns:
            Dict[str, Any]: 트렌드 데이터
        """
        try:
            now = datetime.now()
            
            # 기간에 따른 시간 간격 설정
            if period == "1d":
                delta = timedelta(hours=1)
                points = 24
            elif period == "1w":
                delta = timedelta(hours=6)
                points = 28
            elif period == "1m":
                delta = timedelta(days=1)
                points = 30
            elif period == "3m":
                delta = timedelta(days=3)
                points = 30
            else:
                delta = timedelta(days=1)
                points = 30
            
            # 시장 트렌드 데이터 생성
            trends = []
            market_cap_value = 2e12
            volume_value = 1e11
            btc_dom_value = 45
            
            for i in range(points):
                timestamp = now - (delta * (points - i - 1))
                
                # 랜덤 변동 추가
                market_cap_change = market_cap_value * random.uniform(-0.02, 0.02)
                volume_change = volume_value * random.uniform(-0.05, 0.05)
                btc_dom_change = random.uniform(-0.5, 0.5)
                
                market_cap_value += market_cap_change
                volume_value += volume_change
                btc_dom_value += btc_dom_change
                
                # 값 보정
                btc_dom_value = max(35, min(70, btc_dom_value))
                market_cap_value = max(1.5e12, market_cap_value)
                volume_value = max(5e10, volume_value)
                
                trends.append({
                    "timestamp": timestamp.isoformat(),
                    "market_cap": market_cap_value,
                    "volume_24h": volume_value,
                    "btc_dominance": btc_dom_value
                })
            
            return {
                "period": period,
                "trends": trends,
                "updated_at": now.isoformat()
            }
        except Exception as e:
            self.logger.error(f"시장 트렌드 가져오기 실패: {str(e)}")
            return {"error": str(e)}
    
    def get_correlation_matrix(self, symbols: List[str] = None) -> Dict[str, Any]:
        """
        코인 간 상관관계 매트릭스를 가져옵니다.
        
        Args:
            symbols: 분석할 코인 심볼 목록
            
        Returns:
            Dict[str, Any]: 상관관계 데이터
        """
        try:
            # 기본 심볼 목록
            default_symbols = ["BTC", "ETH", "BNB", "SOL", "XRP", "ADA", "DOT", "AVAX"]
            symbols = symbols or default_symbols
            
            # 상관관계 매트릭스 생성
            matrix = []
            
            for i, symbol1 in enumerate(symbols):
                row = []
                for j, symbol2 in enumerate(symbols):
                    if i == j:
                        correlation = 1.0
                    else:
                        # 비트코인과 이더리움은 높은 상관관계 유지
                        if (symbol1 == "BTC" and symbol2 == "ETH") or (symbol1 == "ETH" and symbol2 == "BTC"):
                            correlation = 0.7 + random.uniform(-0.1, 0.1)
                        else:
                            correlation = random.uniform(-0.2, 0.9)
                    
                    row.append(round(correlation, 2))
                matrix.append(row)
            
            return {
                "symbols": symbols,
                "matrix": matrix,
                "updated_at": datetime.now().isoformat()
            }
        except Exception as e:
            self.logger.error(f"상관관계 매트릭스 가져오기 실패: {str(e)}")
            return {"error": str(e)} 