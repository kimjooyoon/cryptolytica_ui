"""
블록체인 데이터 관련 유틸리티 함수
"""
from datetime import datetime
from typing import Dict, Any, List


def format_blockchain_status(status: str) -> str:
    """블록체인 상태 포맷팅"""
    status_map = {
        "synced": "동기화됨",
        "syncing": "동기화 중",
        "error": "오류"
    }
    return status_map.get(status, status)


def format_transaction_hash(tx_hash: str, max_length: int = 16) -> str:
    """트랜잭션 해시 포맷팅 (축약)"""
    if len(tx_hash) <= max_length:
        return tx_hash
    return f"{tx_hash[:max_length//2]}...{tx_hash[-max_length//2:]}"


def format_address(address: str, max_length: int = 12) -> str:
    """블록체인 주소 포맷팅 (축약)"""
    if len(address) <= max_length:
        return address
    return f"{address[:max_length//2]}...{address[-max_length//2:]}"


def categorize_transaction_volume(volume: float) -> str:
    """거래량 카테고리화"""
    if volume < 1000:
        return "소액"
    elif volume < 100000:
        return "중간"
    elif volume < 1000000:
        return "대액"
    else:
        return "초대액"


def calculate_transaction_stats(transactions: List[Dict[str, Any]]) -> Dict[str, Any]:
    """트랜잭션 통계 계산"""
    if not transactions:
        return {
            "total_count": 0,
            "avg_fee": 0,
            "max_fee": 0,
            "min_fee": 0
        }
    
    total_count = len(transactions)
    fees = [tx.get("fee", 0) for tx in transactions]
    
    return {
        "total_count": total_count,
        "avg_fee": sum(fees) / total_count if total_count > 0 else 0,
        "max_fee": max(fees) if fees else 0,
        "min_fee": min(fees) if fees else 0
    } 