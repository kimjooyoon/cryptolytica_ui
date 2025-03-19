import requests
import json
import websocket
import threading
import time
import logging
from typing import Dict, List, Any, Optional, Callable
from datetime import datetime

from api.models import (
    SystemStatus, Exchange, Blockchain, MarketData, OHLCV,
    Portfolio, AnalysisResult, Event, 
    BlockchainTransaction, WalletActivity, ContractActivity
)

# 로깅 설정
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class CryptoLyticaClient:
    """CryptoLytica API 클라이언트"""
    
    def __init__(self, base_url: str, api_key: str, ws_url: str = None):
        """
        CryptoLytica API 클라이언트 초기화
        
        Args:
            base_url: API 기본 URL (예: "http://localhost:8000")
            api_key: API 키
            ws_url: WebSocket URL (기본값은 None이며, WebSocket을 사용하지 않음)
        """
        self.base_url = base_url.rstrip('/')
        self.api_key = api_key
        self.ws_url = ws_url
        self.ws = None
        self.ws_thread = None
        self.ws_callbacks = {}
        self.logger = logging.getLogger("cryptolytica_client")
    
    def _get_headers(self) -> Dict[str, str]:
        """API 요청에 사용할 헤더 반환"""
        return {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "Accept": "application/json"
        }
    
    def _request(self, method: str, endpoint: str, params: Dict = None, data: Dict = None) -> Dict:
        """
        API 요청 수행
        
        Args:
            method: HTTP 메서드 (GET, POST, PUT, DELETE)
            endpoint: API 엔드포인트
            params: URL 파라미터 (선택적)
            data: 요청 본문 데이터 (선택적)
        
        Returns:
            Dict: API 응답 데이터
        """
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        headers = self._get_headers()
        
        try:
            response = requests.request(
                method=method,
                url=url,
                headers=headers,
                params=params,
                json=data
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            self.logger.error(f"API 요청 오류: {str(e)}")
            # 간단한 응답 생성 (실제 구현에서는 더 자세한 오류 처리가 필요할 수 있음)
            return {"error": str(e)}
    
    def get_system_status(self) -> SystemStatus:
        """
        시스템 상태 정보 가져오기
        
        Returns:
            SystemStatus: 시스템 상태 정보
        """
        # 데모용 가상 데이터 생성
        data = {
            "status": "running",
            "version": "1.0.0",
            "uptime": "5d 12h 30m",
            "collectors": {
                "exchange": "running",
                "blockchain": "running"
            },
            "processors": {
                "market": "running",
                "portfolio": "running"
            },
            "database": {
                "status": "connected",
                "size": "1.2 GB"
            },
            "cpu_usage": 32.5,
            "memory_usage": 42.8,
            "disk_usage": 68.3,
            "last_update": datetime.now().isoformat()
        }
        
        return SystemStatus.from_dict(data)
    
    def get_exchanges(self) -> List[Exchange]:
        """
        지원되는 거래소 목록 가져오기
        
        Returns:
            List[Exchange]: 거래소 목록
        """
        # 데모용 가상 데이터 생성
        data = [
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
        
        return [Exchange.from_dict(item) for item in data]
    
    def get_blockchains(self) -> List[Dict[str, Any]]:
        """
        지원되는 블록체인 목록 가져오기
        
        Returns:
            List[Blockchain]: 블록체인 목록
        """
        # 데모용 가상 데이터 생성
        data = [
            {
                "id": "bitcoin",
                "name": "Bitcoin",
                "status": "synced",
                "last_block": 830000,
                "last_update": datetime.now().isoformat(),
                "network_info": {
                    "hashrate": "180 EH/s",
                    "difficulty": 62.77,
                    "active_addresses": 1200000
                }
            },
            {
                "id": "ethereum",
                "name": "Ethereum",
                "status": "synced",
                "last_block": 19500000,
                "last_update": datetime.now().isoformat(),
                "network_info": {
                    "gas_price": "25 Gwei",
                    "staked_eth": "30M ETH",
                    "active_addresses": 2500000
                }
            },
            {
                "id": "solana",
                "name": "Solana",
                "status": "synced",
                "last_block": 245000000,
                "last_update": datetime.now().isoformat(),
                "network_info": {
                    "transactions_per_second": 2500,
                    "active_validators": 1850,
                    "active_addresses": 950000
                }
            },
            {
                "id": "cardano",
                "name": "Cardano",
                "status": "synced",
                "last_block": 9800000,
                "last_update": datetime.now().isoformat(),
                "network_info": {
                    "stake_pools": 3500,
                    "total_stake": "32B ADA",
                    "active_addresses": 850000
                }
            }
        ]
        
        return data
    
    def get_blockchain_transactions(self, blockchain_id: str, limit: int = 100) -> List[BlockchainTransaction]:
        """
        블록체인 트랜잭션 데이터 가져오기
        
        Args:
            blockchain_id: 블록체인 ID
            limit: 반환할 항목 수
            
        Returns:
            List[BlockchainTransaction]: 블록체인 트랜잭션 데이터
        """
        # 실제 구현에서는 API 요청을 수행
        # 여기서는 데모를 위해 가상 데이터를 반환
        
        # 여기서는 blockchain_data.py 에서 자체 가상 데이터를 생성하도록 구현했으므로
        # 빈 리스트를 반환합니다.
        return []
    
    def get_wallet_activities(self, blockchain_id: str, address: str = None, limit: int = 10) -> List[WalletActivity]:
        """
        지갑 활동 데이터 가져오기
        
        Args:
            blockchain_id: 블록체인 ID
            address: 지갑 주소 (선택적)
            limit: 반환할 항목 수
            
        Returns:
            List[WalletActivity]: 지갑 활동 데이터
        """
        # 실제 구현에서는 API 요청을 수행
        # 여기서는 데모를 위해 가상 데이터를 반환
        
        # 여기서는 blockchain_data.py 에서 자체 가상 데이터를 생성하도록 구현했으므로
        # 빈 리스트를 반환합니다.
        return []
    
    def get_contract_activities(self, blockchain_id: str, contract_address: str = None, limit: int = 100) -> List[ContractActivity]:
        """
        스마트 컨트랙트 활동 데이터 가져오기
        
        Args:
            blockchain_id: 블록체인 ID
            contract_address: 컨트랙트 주소 (선택적)
            limit: 반환할 항목 수
            
        Returns:
            List[ContractActivity]: 스마트 컨트랙트 활동 데이터
        """
        # 실제 구현에서는 API 요청을 수행
        # 여기서는 데모를 위해 가상 데이터를 반환
        
        # 여기서는 blockchain_data.py 에서 자체 가상 데이터를 생성하도록 구현했으므로
        # 빈 리스트를 반환합니다.
        return []
    
    def get_market_data(self, exchange: str = None, symbol: str = None) -> List[MarketData]:
        """
        시장 데이터 가져오기
        
        Args:
            exchange: 거래소 ID (선택적)
            symbol: 거래 쌍 (선택적)
            
        Returns:
            List[MarketData]: 시장 데이터
        """
        # 데모용 가상 데이터 생성
        data = [
            {
                "market_id": "BTC_USDT",
                "exchange": "binance",
                "base_currency": "BTC",
                "quote_currency": "USDT",
                "price": 65420.5,
                "volume_24h": 1245788923.45,
                "high_24h": 65900.0,
                "low_24h": 64200.0,
                "price_change_pct_24h": 2.35,
                "timestamp": datetime.now().isoformat()
            },
            {
                "market_id": "ETH_USDT",
                "exchange": "binance",
                "base_currency": "ETH",
                "quote_currency": "USDT",
                "price": 3450.75,
                "volume_24h": 987654321.0,
                "high_24h": 3500.0,
                "low_24h": 3380.0,
                "price_change_pct_24h": 1.85,
                "timestamp": datetime.now().isoformat()
            }
        ]
        
        return [MarketData.from_dict(item) for item in data]
    
    def get_ohlcv(self, exchange: str, symbol: str, interval: str = "1d", limit: int = 30) -> List[OHLCV]:
        """
        OHLCV 데이터 가져오기
        
        Args:
            exchange: 거래소 ID
            symbol: 거래 쌍
            interval: 간격 (1m, 5m, 15m, 1h, 4h, 1d 등)
            limit: 반환할 항목 수
            
        Returns:
            List[OHLCV]: OHLCV 데이터
        """
        # 여기서는 데모용 가상 데이터를 생성
        data = []
        now = datetime.now()
        
        for i in range(limit):
            timestamp = now - (limit - i) * {
                "1m": {'minutes': 1},
                "5m": {'minutes': 5},
                "15m": {'minutes': 15},
                "1h": {'hours': 1},
                "4h": {'hours': 4},
                "1d": {'days': 1}
            }.get(interval, {'days': 1})
            
            # 가상 데이터 생성
            item = {
                "market_id": f"{symbol}",
                "exchange": exchange,
                "timestamp": timestamp.isoformat(),
                "open": 50000 + i * 100,
                "high": 50000 + i * 100 + 200,
                "low": 50000 + i * 100 - 100,
                "close": 50000 + i * 100 + 50,
                "volume": 1000000 + i * 10000
            }
            data.append(item)
        
        return [OHLCV.from_dict(item) for item in data]
    
    def get_portfolios(self) -> List[Portfolio]:
        """
        사용자 포트폴리오 목록 가져오기
        
        Returns:
            List[Portfolio]: 포트폴리오 목록
        """
        # 데모용 가상 데이터 생성
        data = [
            {
                "id": "portfolio1",
                "name": "메인 포트폴리오",
                "assets": [
                    {
                        "symbol": "BTC",
                        "amount": 1.5,
                        "value_usd": 98000.0,
                        "allocation_pct": 60.0
                    },
                    {
                        "symbol": "ETH",
                        "amount": 15.0,
                        "value_usd": 50000.0,
                        "allocation_pct": 30.0
                    },
                    {
                        "symbol": "SOL",
                        "amount": 200.0,
                        "value_usd": 16000.0,
                        "allocation_pct": 10.0
                    }
                ],
                "total_value": 164000.0,
                "last_update": datetime.now().isoformat()
            },
            {
                "id": "portfolio2",
                "name": "장기 투자",
                "assets": [
                    {
                        "symbol": "BTC",
                        "amount": 0.5,
                        "value_usd": 32500.0,
                        "allocation_pct": 65.0
                    },
                    {
                        "symbol": "ETH",
                        "amount": 5.0,
                        "value_usd": 17500.0,
                        "allocation_pct": 35.0
                    }
                ],
                "total_value": 50000.0,
                "last_update": datetime.now().isoformat()
            }
        ]
        
        return [Portfolio.from_dict(item) for item in data]
    
    def get_analysis_results(self, analysis_type: str = None, limit: int = 10) -> List[AnalysisResult]:
        """
        분석 결과 가져오기
        
        Args:
            analysis_type: 분석 유형 (선택적)
            limit: 반환할 항목 수
            
        Returns:
            List[AnalysisResult]: 분석 결과
        """
        # 데모용 가상 데이터 생성
        data = [
            {
                "id": "analysis1",
                "analysis_type": "technical",
                "timestamp": datetime.now().isoformat(),
                "parameters": {
                    "symbol": "BTC/USDT",
                    "period": "1d"
                },
                "results": {
                    "rsi": 62.5,
                    "macd": 120.5,
                    "ema_50": 64800.0,
                    "ema_200": 58200.0,
                    "trend": "bullish"
                }
            },
            {
                "id": "analysis2",
                "analysis_type": "sentiment",
                "timestamp": datetime.now().isoformat(),
                "parameters": {
                    "symbol": "BTC",
                    "sources": ["twitter", "reddit"]
                },
                "results": {
                    "sentiment_score": 0.75,
                    "volume": 12500,
                    "positive_ratio": 0.68,
                    "negative_ratio": 0.15,
                    "neutral_ratio": 0.17
                }
            }
        ]
        
        return [AnalysisResult.from_dict(item) for item in data]
    
    def get_events(self, severity: str = None, limit: int = 10) -> List[Event]:
        """
        시스템 이벤트 가져오기
        
        Args:
            severity: 이벤트 심각도 (선택적: info, warning, error, critical)
            limit: 반환할 항목 수
            
        Returns:
            List[Event]: 이벤트 목록
        """
        # 데모용 가상 데이터 생성
        data = [
            {
                "id": "event1",
                "event_type": "api_error",
                "source": "binance_collector",
                "severity": "warning",
                "timestamp": datetime.now().isoformat(),
                "message": "Binance API 비정상적 응답",
                "details": {
                    "status_code": 429,
                    "retry_after": 60
                }
            },
            {
                "id": "event2",
                "event_type": "price_alert",
                "source": "alert_system",
                "severity": "info",
                "timestamp": datetime.now().isoformat(),
                "message": "BTC 가격 65,000 USDT 돌파",
                "details": {
                    "symbol": "BTC/USDT",
                    "price": 65420.5,
                    "threshold": 65000.0
                }
            }
        ]
        
        return [Event.from_dict(item) for item in data]
    
    def connect_websocket(self, callback: Callable[[Dict], None] = None) -> bool:
        """
        웹소켓 연결 설정
        
        Args:
            callback: 웹소켓 메시지를 처리할 콜백 함수
            
        Returns:
            bool: 연결 성공 여부
        """
        if not self.ws_url:
            self.logger.error("WebSocket URL이 설정되지 않았습니다.")
            return False
        
        def on_message(ws, message):
            try:
                data = json.loads(message)
                channel = data.get("channel", "default")
                
                # 기본 콜백 호출
                if callback:
                    callback(data)
                
                # 채널별 콜백 호출
                if channel in self.ws_callbacks:
                    for cb in self.ws_callbacks[channel]:
                        cb(data)
            except json.JSONDecodeError:
                self.logger.error("WebSocket 메시지 파싱 오류")
            except Exception as e:
                self.logger.error(f"WebSocket 메시지 처리 오류: {str(e)}")
        
        def on_error(ws, error):
            self.logger.error(f"WebSocket 오류: {str(error)}")
        
        def on_close(ws, close_status_code, close_msg):
            self.logger.info("WebSocket 연결 종료")
        
        def on_open(ws):
            self.logger.info("WebSocket 연결 성공")
            # 인증 메시지 전송
            auth_message = {
                "type": "auth",
                "api_key": self.api_key
            }
            ws.send(json.dumps(auth_message))
        
        # WebSocket 연결
        try:
            self.ws = websocket.WebSocketApp(
                self.ws_url,
                on_message=on_message,
                on_error=on_error,
                on_close=on_close,
                on_open=on_open
            )
            
            # 백그라운드 스레드에서 WebSocket 실행
            self.ws_thread = threading.Thread(target=self.ws.run_forever)
            self.ws_thread.daemon = True
            self.ws_thread.start()
            
            return True
        except Exception as e:
            self.logger.error(f"WebSocket 연결 오류: {str(e)}")
            return False
    
    def subscribe_channel(self, channel: str, callback: Callable[[Dict], None]) -> bool:
        """
        특정 채널 구독
        
        Args:
            channel: 채널 이름
            callback: 채널 메시지를 처리할 콜백 함수
            
        Returns:
            bool: 구독 성공 여부
        """
        if not self.ws:
            return False
        
        # 콜백 등록
        if channel not in self.ws_callbacks:
            self.ws_callbacks[channel] = []
        self.ws_callbacks[channel].append(callback)
        
        # 구독 메시지 전송
        subscribe_message = {
            "type": "subscribe",
            "channel": channel
        }
        self.ws.send(json.dumps(subscribe_message))
        
        return True
    
    def disconnect_websocket(self) -> bool:
        """
        웹소켓 연결 종료
        
        Returns:
            bool: 종료 성공 여부
        """
        if self.ws:
            self.ws.close()
            self.ws = None
            return True
        return False 