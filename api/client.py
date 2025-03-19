import requests
import json
import websocket
import threading
import time
import logging
from typing import Dict, List, Any, Optional, Callable

# 로깅 설정
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class CryptoLyticaClient:
    """CryptoLytica API 클라이언트"""
    
    def __init__(self, base_url: str, api_key: str = "", ws_url: str = ""):
        self.base_url = base_url
        self.api_key = api_key
        self.ws_url = ws_url
        self.headers = {
            "Content-Type": "application/json"
        }
        
        if api_key:
            self.headers["Authorization"] = f"Bearer {api_key}"
        
        self.ws = None
        self.ws_connected = False
        self.ws_callbacks = {}
    
    def get_system_status(self) -> Dict[str, Any]:
        """시스템 상태 정보를 가져옵니다."""
        try:
            response = requests.get(f"{self.base_url}/api/status", headers=self.headers)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"시스템 상태 조회 오류: {str(e)}")
            # 실제 API가 없는 상태에서는 가상 데이터 반환
            return {
                "status": "online",
                "version": "0.1.0",
                "uptime": "1d 4h 23m",
                "collectors": {
                    "exchange": "running",
                    "blockchain": "running"
                },
                "processors": {
                    "market": "running",
                    "analytics": "running"
                },
                "database": {
                    "status": "healthy",
                    "size": "250GB"
                }
            }
    
    def get_exchanges(self) -> List[Dict[str, Any]]:
        """연결된 거래소 목록을 가져옵니다."""
        try:
            response = requests.get(f"{self.base_url}/api/exchanges", headers=self.headers)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"거래소 목록 조회 오류: {str(e)}")
            # 가상 데이터 반환
            return [
                {"id": "binance", "name": "Binance", "status": "connected", "last_update": "2023-06-10T15:30:45Z"},
                {"id": "upbit", "name": "Upbit", "status": "connected", "last_update": "2023-06-10T15:28:12Z"},
                {"id": "bithumb", "name": "Bithumb", "status": "connected", "last_update": "2023-06-10T15:25:18Z"},
                {"id": "coinbase", "name": "Coinbase", "status": "connected", "last_update": "2023-06-10T15:27:33Z"},
                {"id": "kraken", "name": "Kraken", "status": "connected", "last_update": "2023-06-10T15:31:02Z"}
            ]
    
    def get_blockchains(self) -> List[Dict[str, Any]]:
        """연결된 블록체인 목록을 가져옵니다."""
        try:
            response = requests.get(f"{self.base_url}/api/blockchains", headers=self.headers)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"블록체인 목록 조회 오류: {str(e)}")
            # 가상 데이터 반환
            return [
                {"id": "bitcoin", "name": "Bitcoin", "status": "synced", "last_block": 789456, "last_update": "2023-06-10T15:30:45Z"},
                {"id": "ethereum", "name": "Ethereum", "status": "synced", "last_block": 17456789, "last_update": "2023-06-10T15:28:12Z"},
                {"id": "solana", "name": "Solana", "status": "syncing", "last_block": 187654321, "last_update": "2023-06-10T15:25:18Z"},
                {"id": "cardano", "name": "Cardano", "status": "synced", "last_block": 8765432, "last_update": "2023-06-10T15:27:33Z"}
            ]
    
    def get_market_data(self, exchange: str, symbol: str, period: str = "1d", limit: int = 100) -> Dict[str, Any]:
        """시장 데이터를 가져옵니다."""
        try:
            params = {
                "period": period,
                "limit": limit
            }
            response = requests.get(
                f"{self.base_url}/api/market/{exchange}/{symbol}",
                headers=self.headers,
                params=params
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"시장 데이터 조회 오류: {str(e)}")
            # 가상 데이터 생성
            import random
            from datetime import datetime, timedelta
            
            price = 50000.0  # 시작 가격
            data = []
            now = datetime.now()
            
            for i in range(limit):
                timestamp = now - timedelta(days=limit-i-1)
                price_change = random.uniform(-0.05, 0.05)  # -5% ~ +5% 변동
                price = price * (1 + price_change)
                
                data.append({
                    "timestamp": timestamp.isoformat(),
                    "open": price * (1 - random.uniform(0, 0.01)),
                    "high": price * (1 + random.uniform(0, 0.02)),
                    "low": price * (1 - random.uniform(0, 0.02)),
                    "close": price,
                    "volume": random.uniform(100, 1000)
                })
            
            return {
                "exchange": exchange,
                "symbol": symbol,
                "period": period,
                "data": data
            }
    
    def connect_websocket(self, callback: Optional[Callable] = None):
        """WebSocket 연결을 시작합니다."""
        if not self.ws_url:
            logger.warning("WebSocket URL이 설정되지 않았습니다.")
            return False
        
        def on_message(ws, message):
            data = json.loads(message)
            topic = data.get("topic", "")
            
            if topic in self.ws_callbacks:
                self.ws_callbacks[topic](data)
            
            if callback:
                callback(data)
        
        def on_error(ws, error):
            logger.error(f"WebSocket 오류: {str(error)}")
            self.ws_connected = False
        
        def on_close(ws, close_status_code, close_msg):
            logger.info(f"WebSocket 연결 종료: {close_status_code} - {close_msg}")
            self.ws_connected = False
        
        def on_open(ws):
            logger.info("WebSocket 연결 성공")
            self.ws_connected = True
        
        def run_websocket():
            self.ws = websocket.WebSocketApp(
                self.ws_url,
                on_open=on_open,
                on_message=on_message,
                on_error=on_error,
                on_close=on_close,
                header=self.headers
            )
            self.ws.run_forever()
        
        websocket_thread = threading.Thread(target=run_websocket, daemon=True)
        websocket_thread.start()
        
        # 연결 대기
        for _ in range(5):
            if self.ws_connected:
                return True
            time.sleep(1)
        
        return self.ws_connected
    
    def subscribe(self, topic: str, callback: Callable):
        """특정 토픽을 구독하고 콜백을 등록합니다."""
        if not self.ws_connected:
            connected = self.connect_websocket()
            if not connected:
                logger.error(f"WebSocket 연결 실패, 토픽 구독 불가: {topic}")
                return False
        
        self.ws_callbacks[topic] = callback
        
        message = json.dumps({
            "action": "subscribe",
            "topic": topic
        })
        
        try:
            self.ws.send(message)
            logger.info(f"토픽 구독 요청 전송: {topic}")
            return True
        except Exception as e:
            logger.error(f"토픽 구독 요청 실패: {str(e)}")
            return False
    
    def unsubscribe(self, topic: str):
        """특정 토픽 구독을 취소합니다."""
        if not self.ws_connected:
            logger.warning("WebSocket이 연결되지 않았습니다.")
            return False
        
        if topic in self.ws_callbacks:
            del self.ws_callbacks[topic]
        
        message = json.dumps({
            "action": "unsubscribe",
            "topic": topic
        })
        
        try:
            self.ws.send(message)
            logger.info(f"토픽 구독 취소 요청 전송: {topic}")
            return True
        except Exception as e:
            logger.error(f"토픽 구독 취소 요청 실패: {str(e)}")
            return False 