"""
블록체인 데이터 관련 모델 정의
"""
from dataclasses import dataclass
from datetime import datetime
from typing import List, Dict, Optional, Any


@dataclass
class Blockchain:
    """블록체인 네트워크 정보"""
    id: str
    name: str
    status: str
    last_block: int
    last_update: datetime

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Blockchain':
        """딕셔너리에서 Blockchain 객체 생성"""
        return cls(
            id=data["id"],
            name=data["name"],
            status=data["status"],
            last_block=data["last_block"],
            last_update=datetime.fromisoformat(data["last_update"].replace('Z', '+00:00'))
        )


@dataclass
class BlockchainTransaction:
    """블록체인 트랜잭션 통계"""
    timestamp: datetime
    tx_count: int
    avg_fee: float
    block_size: float
    active_addresses: int
    network_hashrate: Optional[float] = None


@dataclass
class WalletActivity:
    """지갑 활동 정보"""
    address: str
    timestamp: datetime
    amount: float
    direction: str
    transaction_hash: str
    activity_type: str


@dataclass
class ContractActivity:
    """스마트 컨트랙트 활동 정보"""
    timestamp: datetime
    contract_address: str
    activity_type: str
    volume: float
    transaction_count: int
    unique_users: int 