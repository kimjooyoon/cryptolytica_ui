import sys
import random
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
from pathlib import Path

# 상위 디렉토리 추가
ROOT_DIR = Path(__file__).parent.parent.parent.parent
sys.path.append(str(ROOT_DIR))

from shared.services.base_client import BaseApiClient
from shared.models.common_models import Exchange, MarketData, OHLCV

class ExchangeClient(BaseApiClient):
    """거래소 데이터 API 클라이언트"""
    
    def __init__(self, base_url: str, api_key: str = "", ws_url: str = ""):
        """
        ExchangeClient 초기화
        
        Args:
            base_url: API 기본 URL
            api_key: API 키
            ws_url: WebSocket URL
        """
        super().__init__(base_url, api_key, ws_url)
    
    def get_exchanges(self) -> List[Dict[str, Any]]:
        """
        사용 가능한 거래소 목록을 가져옵니다.
        
        Returns:
            List[Dict[str, Any]]: 거래소 정보 목록
        """
        try:
            # 실제 API 호출 대신 데모 데이터 생성
            return [
                {
                    "id": "binance",
                    "name": "Binance",
                    "status": "active",
                    "supported_markets": ["BTC/USDT", "ETH/USDT", "SOL/USDT"],
                    "api_status": "operational",
                    "last_update": datetime.now().isoformat()
                },
                {
                    "id": "coinbase",
                    "name": "Coinbase",
                    "status": "active",
                    "supported_markets": ["BTC/USD", "ETH/USD"],
                    "api_status": "operational",
                    "last_update": datetime.now().isoformat()
                },
                {
                    "id": "upbit",
                    "name": "Upbit",
                    "status": "active",
                    "supported_markets": ["BTC/KRW", "ETH/KRW"],
                    "api_status": "operational",
                    "last_update": datetime.now().isoformat()
                }
            ]
        except Exception as e:
            self.logger.error(f"거래소 목록 가져오기 실패: {str(e)}")
            # 오류 시 빈 목록 반환
            return []
    
    def get_exchange_by_id(self, exchange_id: str) -> Optional[Dict[str, Any]]:
        """
        ID로 특정 거래소 정보를 가져옵니다.
        
        Args:
            exchange_id: 거래소 ID
            
        Returns:
            Optional[Dict[str, Any]]: 거래소 정보
        """
        try:
            # 모든 거래소 가져와서 필터링
            exchanges = self.get_exchanges()
            for exchange in exchanges:
                if exchange.get("id") == exchange_id:
                    return exchange
            return None
        except Exception as e:
            self.logger.error(f"거래소 정보 가져오기 실패: {str(e)}")
            return None
    
    def get_market_data(self, exchange_id: str, symbol: str, period: str = "1d", limit: int = 100) -> Dict[str, Any]:
        """
        특정 거래소와 심볼에 대한 시장 데이터를 가져옵니다.
        
        Args:
            exchange_id: 거래소 ID
            symbol: 통화쌍 심볼 (예: "BTC/USDT")
            period: 데이터 기간 (예: "1h", "4h", "1d")
            limit: 최대 데이터 수
            
        Returns:
            Dict[str, Any]: 시장 데이터
        """
        try:
            # 실제 API 호출 대신 가상 데이터 생성
            end_time = datetime.now()
            
            # 기간에 따른 시간 간격 설정
            if period == "1h":
                delta = timedelta(hours=1)
            elif period == "4h":
                delta = timedelta(hours=4)
            elif period == "1d":
                delta = timedelta(days=1)
            elif period == "1w":
                delta = timedelta(weeks=1)
            elif period == "1M":
                delta = timedelta(days=30)
            else:
                delta = timedelta(days=1)
            
            # 시작 시간 계산
            start_time = end_time - (delta * limit)
            
            # 기본 가격 설정 (심볼에 따라 다름)
            if "BTC" in symbol:
                base_price = 50000
                volatility = 0.03
            elif "ETH" in symbol:
                base_price = 3000
                volatility = 0.04
            elif "SOL" in symbol:
                base_price = 100
                volatility = 0.05
            else:
                base_price = 10
                volatility = 0.03
            
            # 데이터 생성
            data = []
            current_time = start_time
            current_price = base_price
            
            while current_time <= end_time:
                # 가격 변동 생성
                price_change = current_price * random.uniform(-volatility, volatility)
                current_price += price_change
                
                # 고가, 저가 생성
                high_price = current_price * (1 + random.uniform(0, volatility/2))
                low_price = current_price * (1 - random.uniform(0, volatility/2))
                
                # 시가, 종가 생성
                open_price = current_price - (price_change * random.uniform(0, 1))
                close_price = current_price
                
                # 거래량 생성
                volume = base_price * 10 * random.uniform(0.5, 5)
                
                # 데이터 추가
                data.append({
                    "timestamp": current_time.isoformat(),
                    "open": open_price,
                    "high": high_price,
                    "low": low_price,
                    "close": close_price,
                    "volume": volume
                })
                
                # 다음 시간으로 이동
                current_time += delta
            
            # 최종 데이터 반환
            return {
                "exchange": exchange_id,
                "symbol": symbol,
                "period": period,
                "data": data
            }
        except Exception as e:
            self.logger.error(f"시장 데이터 가져오기 실패: {str(e)}")
            return {"error": str(e)}
    
    def get_tickers(self, exchange_id: str) -> List[Dict[str, Any]]:
        """
        특정 거래소의 모든 티커 정보를 가져옵니다.
        
        Args:
            exchange_id: 거래소 ID
            
        Returns:
            List[Dict[str, Any]]: 티커 정보 목록
        """
        try:
            # 거래소별 기본 티커 목록
            base_tickers = {
                "binance": ["BTC/USDT", "ETH/USDT", "SOL/USDT", "ADA/USDT", "DOT/USDT"],
                "coinbase": ["BTC/USD", "ETH/USD", "SOL/USD", "LINK/USD"],
                "upbit": ["BTC/KRW", "ETH/KRW", "XRP/KRW", "ADA/KRW"]
            }
            
            tickers = base_tickers.get(exchange_id, ["BTC/USDT", "ETH/USDT"])
            result = []
            
            for ticker in tickers:
                # 기본 가격 설정
                if "BTC" in ticker:
                    price = 50000 + random.uniform(-1000, 1000)
                    volume = 1000 + random.uniform(-200, 200)
                elif "ETH" in ticker:
                    price = 3000 + random.uniform(-100, 100)
                    volume = 5000 + random.uniform(-500, 500)
                elif "SOL" in ticker:
                    price = 100 + random.uniform(-5, 5)
                    volume = 20000 + random.uniform(-2000, 2000)
                else:
                    price = 10 + random.uniform(-1, 1)
                    volume = 50000 + random.uniform(-5000, 5000)
                
                # 변동률 계산
                change_24h = random.uniform(-0.05, 0.05)
                
                result.append({
                    "symbol": ticker,
                    "price": price,
                    "volume_24h": volume,
                    "change_24h": change_24h,
                    "high_24h": price * (1 + random.uniform(0, 0.03)),
                    "low_24h": price * (1 - random.uniform(0, 0.03)),
                    "updated_at": datetime.now().isoformat()
                })
            
            return result
        except Exception as e:
            self.logger.error(f"티커 정보 가져오기 실패: {str(e)}")
            return []
    
    def subscribe_to_ticker(self, exchange_id: str, symbol: str, callback: callable) -> bool:
        """
        특정 티커의 실시간 업데이트를 구독합니다.
        
        Args:
            exchange_id: 거래소 ID
            symbol: 심볼 (예: "BTC/USDT")
            callback: 데이터 수신 시 호출될 콜백 함수
            
        Returns:
            bool: 구독 성공 여부
        """
        if not self.ws_url:
            self.logger.warning("WebSocket URL이 설정되지 않아 구독할 수 없습니다.")
            return False
        
        try:
            # WebSocket 연결 확인 및 생성
            if not self.ws:
                self.connect_websocket()
            
            # 채널 이름 생성
            channel = f"{exchange_id}.ticker.{symbol}"
            
            # 채널 구독
            if self.ws and self.ws.sock and self.ws.sock.connected:
                # 구독 메시지 전송
                subscribe_msg = {
                    "type": "subscribe",
                    "channel": channel
                }
                self.ws.send(json.dumps(subscribe_msg))
                
                # 콜백 등록
                self.subscribe_channel(channel, callback)
                self.logger.info(f"티커 {symbol} 구독 성공 (거래소: {exchange_id})")
                return True
            else:
                self.logger.error("WebSocket이 연결되어 있지 않습니다.")
                return False
        except Exception as e:
            self.logger.error(f"티커 구독 실패: {str(e)}")
            return False 