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
class ApiResponse:
    """API 응답 기본 형식"""
    success: bool
    data: Any
    message: Optional[str] = None
    errors: Optional[List[Dict[str, Any]]] = None
    timestamp: datetime = None

    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.now()

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'ApiResponse':
        timestamp = data.get('timestamp')
        if timestamp and isinstance(timestamp, str):
            timestamp = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
        
        return cls(
            success=data.get('success', False),
            data=data.get('data'),
            message=data.get('message'),
            errors=data.get('errors'),
            timestamp=timestamp
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
        timestamp = data.get('timestamp')
        if isinstance(timestamp, str):
            timestamp = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
        elif timestamp is None:
            timestamp = datetime.now()
            
        return cls(
            id=data.get('id', ''),
            event_type=data.get('event_type', ''),
            source=data.get('source', ''),
            severity=data.get('severity', 'info'),
            timestamp=timestamp,
            message=data.get('message', ''),
            details=data.get('details', {})
        )

@dataclass
class PageInfo:
    """페이지네이션 정보"""
    page: int
    page_size: int
    total_items: int
    total_pages: int
    has_next: bool
    has_prev: bool
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'PageInfo':
        page = data.get('page', 1)
        page_size = data.get('page_size', 10)
        total_items = data.get('total_items', 0)
        
        # 전체 페이지 수 계산
        total_pages = (total_items + page_size - 1) // page_size if page_size > 0 else 0
        
        return cls(
            page=page,
            page_size=page_size,
            total_items=total_items,
            total_pages=total_pages,
            has_next=page < total_pages,
            has_prev=page > 1
        )

@dataclass
class OHLCV:
    """OHLCV 데이터 (시가, 고가, 저가, 종가, 거래량)"""
    market_id: str
    exchange: str
    timestamp: datetime
    open: float
    high: float
    low: float
    close: float
    volume: float
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'OHLCV':
        timestamp = data.get('timestamp')
        if isinstance(timestamp, str):
            timestamp = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
        
        return cls(
            market_id=data.get('market_id', ''),
            exchange=data.get('exchange', ''),
            timestamp=timestamp or datetime.now(),
            open=float(data.get('open', 0.0)),
            high=float(data.get('high', 0.0)),
            low=float(data.get('low', 0.0)),
            close=float(data.get('close', 0.0)),
            volume=float(data.get('volume', 0.0))
        )

def from_dict(data_class: type, data: Dict[str, Any]) -> Any:
    """딕셔너리에서 데이터 클래스 객체 생성"""
    return data_class(**data) 