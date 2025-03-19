from dataclasses import dataclass
from typing import List, Dict, Any, Optional
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

@dataclass
class Exchange:
    """거래소 정보"""
    id: str
    name: str
    status: str
    last_update: str
    
    @property
    def last_update_dt(self) -> datetime:
        """마지막 업데이트 시간을 datetime 객체로 변환"""
        return datetime.fromisoformat(self.last_update.replace('Z', '+00:00'))

@dataclass
class Blockchain:
    """블록체인 정보"""
    id: str
    name: str
    status: str
    last_block: int
    last_update: str
    
    @property
    def last_update_dt(self) -> datetime:
        """마지막 업데이트 시간을 datetime 객체로 변환"""
        return datetime.fromisoformat(self.last_update.replace('Z', '+00:00'))

@dataclass
class MarketData:
    """시장 데이터"""
    exchange: str
    symbol: str
    period: str
    data: List[Dict[str, Any]]
    
    def to_dataframe(self):
        """pandas DataFrame으로 변환"""
        try:
            import pandas as pd
            df = pd.DataFrame(self.data)
            
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
    assets: List[PortfolioAsset]
    total_value: float
    last_update: str
    
    @property
    def last_update_dt(self) -> datetime:
        """마지막 업데이트 시간을 datetime 객체로 변환"""
        return datetime.fromisoformat(self.last_update.replace('Z', '+00:00'))

@dataclass
class AnalysisResult:
    """분석 결과"""
    analysis_type: str
    symbol: str
    timestamp: str
    data: Dict[str, Any]
    indicators: Dict[str, Any]
    
    @property
    def timestamp_dt(self) -> datetime:
        """타임스탬프를 datetime 객체로 변환"""
        return datetime.fromisoformat(self.timestamp.replace('Z', '+00:00'))

@dataclass
class Event:
    """시스템 이벤트"""
    id: str
    timestamp: str
    event_type: str
    severity: str  # info, warning, error, critical
    message: str
    details: Optional[Dict[str, Any]] = None
    
    @property
    def timestamp_dt(self) -> datetime:
        """타임스탬프를 datetime 객체로 변환"""
        return datetime.fromisoformat(self.timestamp.replace('Z', '+00:00'))

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
    assets = [from_dict(PortfolioAsset, asset) for asset in data.get("assets", [])]
    return Portfolio(
        assets=assets,
        total_value=data.get("total_value", 0.0),
        last_update=data.get("last_update", "")
    )

def analysis_result_from_dict(data: Dict[str, Any]) -> AnalysisResult:
    """딕셔너리에서 AnalysisResult 인스턴스를 생성"""
    return from_dict(AnalysisResult, data)

def event_from_dict(data: Dict[str, Any]) -> Event:
    """딕셔너리에서 Event 인스턴스를 생성"""
    return from_dict(Event, data) 