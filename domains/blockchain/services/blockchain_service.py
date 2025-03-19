"""
블록체인 데이터 관련 서비스 구현
"""
import pandas as pd
import random
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional

from api.client import CryptoLyticaClient
from domains.blockchain.models.blockchain_model import (
    Blockchain, 
    BlockchainTransaction, 
    WalletActivity, 
    ContractActivity
)


class BlockchainService:
    """블록체인 데이터 서비스"""
    
    def __init__(self, client: CryptoLyticaClient):
        self.client = client
    
    def get_blockchains(self) -> List[Dict[str, Any]]:
        """블록체인 목록 가져오기"""
        return self.client.get_blockchains()
    
    def get_blockchain_by_id(self, blockchain_id: str) -> Optional[Dict[str, Any]]:
        """ID로 블록체인 정보 가져오기"""
        blockchains = self.get_blockchains()
        return next((b for b in blockchains if b["id"] == blockchain_id), None)
    
    def get_blockchain_transactions(self, blockchain: str, limit: int = 100) -> pd.DataFrame:
        """블록체인 트랜잭션 데이터 생성 (가상 데이터)"""
        # 가상 데이터 생성
        now = datetime.now()
        
        data = []
        for i in range(limit):
            timestamp = now - timedelta(hours=i)
            
            # 블록체인별로 다른 패턴 생성
            if blockchain == "bitcoin":
                tx_count = 3000 + random.randint(-300, 300)
                avg_fee = 0.0001 + random.uniform(-0.00002, 0.00005)
                block_size = 1.2 + random.uniform(-0.2, 0.3)
            elif blockchain == "ethereum":
                tx_count = 15000 + random.randint(-1500, 1500)
                avg_fee = 0.002 + random.uniform(-0.0005, 0.001)
                block_size = 0.08 + random.uniform(-0.01, 0.02)
            elif blockchain == "solana":
                tx_count = 50000 + random.randint(-5000, 5000)
                avg_fee = 0.00001 + random.uniform(-0.000001, 0.000005)
                block_size = 0.02 + random.uniform(-0.005, 0.005)
            else:
                tx_count = 5000 + random.randint(-500, 500)
                avg_fee = 0.0005 + random.uniform(-0.0001, 0.0001)
                block_size = 0.5 + random.uniform(-0.1, 0.1)
            
            data.append({
                "timestamp": timestamp,
                "tx_count": tx_count,
                "avg_fee": avg_fee,
                "block_size": block_size,
                "active_addresses": int(tx_count * random.uniform(0.2, 0.4)),
                "network_hashrate": random.uniform(100, 200) if blockchain == "bitcoin" else None
            })
        
        return pd.DataFrame(data)
    
    def get_wallet_activities(self, blockchain: str, limit: int = 10) -> pd.DataFrame:
        """지갑 활동 데이터 생성 (가상 데이터)"""
        # 가상 데이터 생성
        now = datetime.now()
        
        # 블록체인별 지갑 주소 형식
        if blockchain == "bitcoin":
            prefix = "bc1"
        elif blockchain == "ethereum":
            prefix = "0x"
        elif blockchain == "solana":
            prefix = "So1"
        else:
            prefix = "addr"
        
        data = []
        for i in range(limit):
            # 무작위 지갑 주소 생성
            address = f"{prefix}{''.join(random.choices('abcdef0123456789', k=40))}"
            
            # 트랜잭션 데이터
            timestamp = now - timedelta(minutes=random.randint(1, 300))
            amount = 10 ** random.uniform(0, 4)  # 0.1 ~ 10000 범위
            direction = random.choice(["in", "out"])
            
            data.append({
                "address": address,
                "timestamp": timestamp,
                "amount": amount,
                "direction": direction,
                "transaction_hash": f"0x{''.join(random.choices('abcdef0123456789', k=64))}",
                "activity_type": random.choice(["transfer", "swap", "stake", "unstake", "mint"])
            })
        
        return pd.DataFrame(data)
    
    def get_contract_activities(self, blockchain: str, limit: int = 100) -> pd.DataFrame:
        """스마트 컨트랙트 활동 데이터 생성 (가상 데이터)"""
        if blockchain not in ["ethereum", "solana", "cardano"]:
            return pd.DataFrame()  # 비어있는 데이터프레임 반환
        
        # 가상 데이터 생성
        now = datetime.now()
        
        data = []
        for i in range(limit):
            timestamp = now - timedelta(hours=i)
            
            if blockchain == "ethereum":
                prefix = "0x"
                activities = ["swap", "liquidity", "mint", "burn", "transfer"]
            elif blockchain == "solana":
                prefix = "So1"
                activities = ["swap", "liquidity", "stake", "unstake", "vote"]
            else:
                prefix = "addr"
                activities = ["transfer", "delegate", "vote", "claim"]
            
            contract_address = f"{prefix}{''.join(random.choices('abcdef0123456789', k=40))}"
            activity_type = random.choice(activities)
            volume = 10 ** random.uniform(2, 6)  # 100 ~ 1,000,000 범위
            
            data.append({
                "timestamp": timestamp,
                "contract_address": contract_address,
                "activity_type": activity_type,
                "volume": volume,
                "transaction_count": int(10 ** random.uniform(1, 3)),  # 10 ~ 1000 범위
                "unique_users": int(10 ** random.uniform(0, 2))  # 1 ~ 100 범위
            })
        
        return pd.DataFrame(data) 