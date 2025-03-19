from dataclasses import dataclass
from typing import List, Dict, Any, Optional, Union
from datetime import datetime

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
    """블록체인 트랜잭션 통계"""
    blockchain_id: str
    timestamp: datetime
    tx_count: int
    avg_fee: float
    block_size: float
    active_addresses: int
    network_hashrate: Optional[float]
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'BlockchainTransaction':
        timestamp = data.get('timestamp')
        if isinstance(timestamp, str):
            timestamp = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
        elif timestamp is None:
            timestamp = datetime.now()
            
        return cls(
            blockchain_id=data.get('blockchain_id', ''),
            timestamp=timestamp,
            tx_count=data.get('tx_count', 0),
            avg_fee=data.get('avg_fee', 0.0),
            block_size=data.get('block_size', 0.0),
            active_addresses=data.get('active_addresses', 0),
            network_hashrate=data.get('network_hashrate')
        )

@dataclass
class WalletActivity:
    """지갑 활동 정보"""
    blockchain_id: str
    address: str
    timestamp: datetime
    amount: float
    direction: str  # 'in' or 'out'
    transaction_hash: str
    activity_type: str
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'WalletActivity':
        timestamp = data.get('timestamp')
        if isinstance(timestamp, str):
            timestamp = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
        elif timestamp is None:
            timestamp = datetime.now()
            
        return cls(
            blockchain_id=data.get('blockchain_id', ''),
            address=data.get('address', ''),
            timestamp=timestamp,
            amount=data.get('amount', 0.0),
            direction=data.get('direction', ''),
            transaction_hash=data.get('transaction_hash', ''),
            activity_type=data.get('activity_type', '')
        )

@dataclass
class ContractActivity:
    """스마트 컨트랙트 활동 정보"""
    blockchain_id: str
    contract_address: str
    timestamp: datetime
    activity_type: str
    volume: float
    transaction_count: int
    unique_users: int
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'ContractActivity':
        timestamp = data.get('timestamp')
        if isinstance(timestamp, str):
            timestamp = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
        elif timestamp is None:
            timestamp = datetime.now()
            
        return cls(
            blockchain_id=data.get('blockchain_id', ''),
            contract_address=data.get('contract_address', ''),
            timestamp=timestamp,
            activity_type=data.get('activity_type', ''),
            volume=data.get('volume', 0.0),
            transaction_count=data.get('transaction_count', 0),
            unique_users=data.get('unique_users', 0)
        )

@dataclass
class Block:
    """블록 정보"""
    blockchain_id: str
    height: int
    hash: str
    timestamp: datetime
    transactions: int
    size: float
    miner: Optional[str] = None
    difficulty: Optional[float] = None
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Block':
        timestamp = data.get('timestamp')
        if isinstance(timestamp, str):
            timestamp = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
        elif timestamp is None:
            timestamp = datetime.now()
            
        return cls(
            blockchain_id=data.get('blockchain_id', ''),
            height=data.get('height', 0),
            hash=data.get('hash', ''),
            timestamp=timestamp,
            transactions=data.get('transactions', 0),
            size=data.get('size', 0.0),
            miner=data.get('miner'),
            difficulty=data.get('difficulty')
        )

@dataclass
class Transaction:
    """트랜잭션 정보"""
    blockchain_id: str
    hash: str
    timestamp: datetime
    from_address: str
    to_address: str
    value: float
    fee: float
    status: str
    block_height: Optional[int] = None
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Transaction':
        timestamp = data.get('timestamp')
        if isinstance(timestamp, str):
            timestamp = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
        elif timestamp is None:
            timestamp = datetime.now()
            
        return cls(
            blockchain_id=data.get('blockchain_id', ''),
            hash=data.get('hash', ''),
            timestamp=timestamp,
            from_address=data.get('from_address', ''),
            to_address=data.get('to_address', ''),
            value=data.get('value', 0.0),
            fee=data.get('fee', 0.0),
            status=data.get('status', ''),
            block_height=data.get('block_height')
        )

@dataclass
class BlockchainNetwork:
    """블록체인 네트워크 정보"""
    blockchain_id: str
    node_count: int
    average_block_time: float
    current_difficulty: float
    hashrate: Optional[float] = None
    staking_apy: Optional[float] = None
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'BlockchainNetwork':
        return cls(
            blockchain_id=data.get('blockchain_id', ''),
            node_count=data.get('node_count', 0),
            average_block_time=data.get('average_block_time', 0.0),
            current_difficulty=data.get('current_difficulty', 0.0),
            hashrate=data.get('hashrate'),
            staking_apy=data.get('staking_apy')
        ) 