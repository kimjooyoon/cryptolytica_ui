from dataclasses import dataclass
from typing import List, Dict, Any, Optional, Union
from datetime import datetime

@dataclass
class SystemStatus:
    """시스템 상태 정보"""
    status: str
    version: str
    uptime: str
    collectors: Dict[str, str]
    processors: Dict[str, str]
    database: Dict[str, Any]
    cpu_usage: float
    memory_usage: float
    disk_usage: float
    last_update: datetime

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'SystemStatus':
        return cls(
            status=data.get('status', 'unknown'),
            version=data.get('version', 'unknown'),
            uptime=data.get('uptime', 'unknown'),
            collectors=data.get('collectors', {}),
            processors=data.get('processors', {}),
            database=data.get('database', {}),
            cpu_usage=data.get('cpu_usage', 0.0),
            memory_usage=data.get('memory_usage', 0.0),
            disk_usage=data.get('disk_usage', 0.0),
            last_update=datetime.fromisoformat(data.get('last_update', datetime.now().isoformat()))
        )

@dataclass
class Exchange:
    """거래소 정보"""
    id: str
    name: str
    status: str
    supported_markets: List[str]
    api_status: str
    last_update: str
    
    @property
    def last_update_dt(self) -> datetime:
        """마지막 업데이트 시간을 datetime 객체로 변환"""
        return datetime.fromisoformat(self.last_update.replace('Z', '+00:00'))

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Exchange':
        return cls(
            id=data.get('id', ''),
            name=data.get('name', ''),
            status=data.get('status', 'unknown'),
            supported_markets=data.get('supported_markets', []),
            api_status=data.get('api_status', 'unknown'),
            last_update=data.get('last_update', '')
        )

@dataclass
class Blockchain:
    """블록체인 정보"""
    id: str
    name: str
    status: str
    last_block: int
    last_update: str
    network_info: Dict[str, Any]
    
    @property
    def last_update_dt(self) -> datetime:
        """마지막 업데이트 시간을 datetime 객체로 변환"""
        return datetime.fromisoformat(self.last_update.replace('Z', '+00:00'))

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Blockchain':
        return cls(
            id=data.get('id', ''),
            name=data.get('name', ''),
            status=data.get('status', 'unknown'),
            last_block=data.get('last_block', 0),
            last_update=data.get('last_update', ''),
            network_info=data.get('network_info', {})
        )

@dataclass
class BlockchainTransaction:
    blockchain_id: str
    timestamp: datetime
    tx_count: int
    avg_fee: float
    block_size: float
    active_addresses: int
    network_hashrate: Optional[float]
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'BlockchainTransaction':
        return cls(
            blockchain_id=data.get('blockchain_id', ''),
            timestamp=datetime.fromisoformat(data.get('timestamp', datetime.now().isoformat())),
            tx_count=data.get('tx_count', 0),
            avg_fee=data.get('avg_fee', 0.0),
            block_size=data.get('block_size', 0.0),
            active_addresses=data.get('active_addresses', 0),
            network_hashrate=data.get('network_hashrate')
        )

@dataclass
class WalletActivity:
    blockchain_id: str
    address: str
    timestamp: datetime
    amount: float
    direction: str  # 'in' or 'out'
    transaction_hash: str
    activity_type: str
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'WalletActivity':
        return cls(
            blockchain_id=data.get('blockchain_id', ''),
            address=data.get('address', ''),
            timestamp=datetime.fromisoformat(data.get('timestamp', datetime.now().isoformat())),
            amount=data.get('amount', 0.0),
            direction=data.get('direction', ''),
            transaction_hash=data.get('transaction_hash', ''),
            activity_type=data.get('activity_type', '')
        )

@dataclass
class ContractActivity:
    blockchain_id: str
    contract_address: str
    timestamp: datetime
    activity_type: str
    volume: float
    transaction_count: int
    unique_users: int
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'ContractActivity':
        return cls(
            blockchain_id=data.get('blockchain_id', ''),
            contract_address=data.get('contract_address', ''),
            timestamp=datetime.fromisoformat(data.get('timestamp', datetime.now().isoformat())),
            activity_type=data.get('activity_type', ''),
            volume=data.get('volume', 0.0),
            transaction_count=data.get('transaction_count', 0),
            unique_users=data.get('unique_users', 0)
        )

@dataclass
class MarketData:
    """시장 데이터"""
    market_id: str
    exchange: str
    base_currency: str
    quote_currency: str
    price: float
    volume_24h: float
    high_24h: float
    low_24h: float
    price_change_pct_24h: float
    timestamp: datetime
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'MarketData':
        return cls(
            market_id=data.get('market_id', ''),
            exchange=data.get('exchange', ''),
            base_currency=data.get('base_currency', ''),
            quote_currency=data.get('quote_currency', ''),
            price=data.get('price', 0.0),
            volume_24h=data.get('volume_24h', 0.0),
            high_24h=data.get('high_24h', 0.0),
            low_24h=data.get('low_24h', 0.0),
            price_change_pct_24h=data.get('price_change_pct_24h', 0.0),
            timestamp=datetime.fromisoformat(data.get('timestamp', datetime.now().isoformat())),
        )

    def to_dataframe(self):
        """pandas DataFrame으로 변환"""
        try:
            import pandas as pd
            df = pd.DataFrame([self.__dict__])
            
            # timestamp를 datetime으로 변환
            df['timestamp'] = pd.to_datetime(df['timestamp'])
            
            return df
        except ImportError:
            raise ImportError("데이터 프레임 변환을 위해 pandas를 설치해주세요: pip install pandas")

@dataclass
class PortfolioAsset:
    """포트폴리오 자산"""
    symbol: str
    amount: float
    price: float
    value: float
    allocation: float  # 포트폴리오 내 비중 (%)
    
    @property
    def total_value(self) -> float:
        """자산의 총 가치"""
        return self.amount * self.price

@dataclass
class Portfolio:
    """포트폴리오 정보"""
    id: str
    name: str
    assets: List[Dict[str, Any]]
    total_value: float
    last_update: datetime
    
    @property
    def last_update_dt(self) -> datetime:
        """마지막 업데이트 시간을 datetime 객체로 변환"""
        return self.last_update

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Portfolio':
        assets = [from_dict(PortfolioAsset, asset) for asset in data.get("assets", [])]
        return cls(
            id=data.get('id', ''),
            name=data.get('name', ''),
            assets=assets,
            total_value=data.get("total_value", 0.0),
            last_update=datetime.fromisoformat(data.get("last_update", datetime.now().isoformat()))
        )

@dataclass
class AnalysisResult:
    """분석 결과"""
    id: str
    analysis_type: str
    timestamp: datetime
    parameters: Dict[str, Any]
    results: Dict[str, Any]
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'AnalysisResult':
        return cls(
            id=data.get('id', ''),
            analysis_type=data.get('analysis_type', ''),
            timestamp=datetime.fromisoformat(data.get('timestamp', datetime.now().isoformat())),
            parameters=data.get('parameters', {}),
            results=data.get('results', {})
        )

@dataclass
class Event:
    """시스템 이벤트"""
    id: str
    event_type: str
    source: str
    severity: str
    timestamp: datetime
    message: str
    details: Dict[str, Any]
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Event':
        return cls(
            id=data.get('id', ''),
            event_type=data.get('event_type', ''),
            source=data.get('source', ''),
            severity=data.get('severity', 'info'),
            timestamp=datetime.fromisoformat(data.get('timestamp', datetime.now().isoformat())),
            message=data.get('message', ''),
            details=data.get('details', {})
        )

def from_dict(data_class, data_dict):
    """딕셔너리에서 데이터 클래스 인스턴스를 생성"""
    return data_class(**data_dict)

def system_status_from_dict(data: Dict[str, Any]) -> SystemStatus:
    """딕셔너리에서 SystemStatus 인스턴스를 생성"""
    return from_dict(SystemStatus, data)

def exchange_from_dict(data: Dict[str, Any]) -> Exchange:
    """딕셔너리에서 Exchange 인스턴스를 생성"""
    return from_dict(Exchange, data)

def blockchain_from_dict(data: Dict[str, Any]) -> Blockchain:
    """딕셔너리에서 Blockchain 인스턴스를 생성"""
    return from_dict(Blockchain, data)

def market_data_from_dict(data: Dict[str, Any]) -> MarketData:
    """딕셔너리에서 MarketData 인스턴스를 생성"""
    return from_dict(MarketData, data)

def portfolio_from_dict(data: Dict[str, Any]) -> Portfolio:
    """딕셔너리에서 Portfolio 인스턴스를 생성"""
    return from_dict(Portfolio, data)

def analysis_result_from_dict(data: Dict[str, Any]) -> AnalysisResult:
    """딕셔너리에서 AnalysisResult 인스턴스를 생성"""
    return from_dict(AnalysisResult, data)

def event_from_dict(data: Dict[str, Any]) -> Event:
    """딕셔너리에서 Event 인스턴스를 생성"""
    return from_dict(Event, data) 