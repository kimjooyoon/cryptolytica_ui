import sys
import logging
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
import random
import pandas as pd
from pathlib import Path

# 상위 디렉토리 경로 추가
ROOT_DIR = Path(__file__).parent.parent.parent.parent
sys.path.append(str(ROOT_DIR))

from shared.services.base_client import BaseApiClient
from domains.blockchain.models.blockchain_models import (
    Blockchain, BlockchainTransaction, WalletActivity, 
    ContractActivity, Block, Transaction, BlockchainNetwork
)

class BlockchainClient(BaseApiClient):
    """블록체인 데이터 API 클라이언트"""
    
    def __init__(self, base_url: str, api_key: str = "", ws_url: str = ""):
        """
        BlockchainClient 초기화
        
        Args:
            base_url: API 기본 URL
            api_key: API 키
            ws_url: WebSocket URL
        """
        super().__init__(base_url, api_key, ws_url)
    
    def get_blockchains(self) -> List[Dict[str, Any]]:
        """
        사용 가능한 블록체인 목록을 가져옵니다.
        
        Returns:
            List[Dict[str, Any]]: 블록체인 정보 목록
        """
        try:
            # 실제 API 호출 대신 데모 데이터 생성
            return [
                {
                    "id": "bitcoin",
                    "name": "비트코인",
                    "status": "synced",
                    "last_block": 820000,
                    "last_update": datetime.now().isoformat(),
                    "network_info": {
                        "hashrate": "450 EH/s",
                        "difficulty": 78349962886.63,
                        "avg_block_time": 10.0
                    }
                },
                {
                    "id": "ethereum",
                    "name": "이더리움",
                    "status": "synced",
                    "last_block": 19150000,
                    "last_update": datetime.now().isoformat(),
                    "network_info": {
                        "staking_apy": "4.2%",
                        "active_validators": 930000,
                        "avg_block_time": 12.1
                    }
                },
                {
                    "id": "solana",
                    "name": "솔라나",
                    "status": "synced",
                    "last_block": 230000000,
                    "last_update": datetime.now().isoformat(),
                    "network_info": {
                        "staking_apy": "6.1%",
                        "active_validators": 2000,
                        "avg_block_time": 0.4
                    }
                },
                {
                    "id": "cardano",
                    "name": "카르다노",
                    "status": "synced",
                    "last_block": 9200000,
                    "last_update": datetime.now().isoformat(),
                    "network_info": {
                        "staking_apy": "3.5%",
                        "active_stake_pools": 3000,
                        "avg_block_time": 20.0
                    }
                }
            ]
        except Exception as e:
            self.logger.error(f"블록체인 목록 가져오기 실패: {str(e)}")
            # 오류 시 빈 목록 반환
            return []
    
    def get_blockchain_by_id(self, blockchain_id: str) -> Optional[Dict[str, Any]]:
        """
        ID로 특정 블록체인 정보를 가져옵니다.
        
        Args:
            blockchain_id: 블록체인 ID
            
        Returns:
            Optional[Dict[str, Any]]: 블록체인 정보
        """
        try:
            # 모든 블록체인 가져와서 필터링
            blockchains = self.get_blockchains()
            for blockchain in blockchains:
                if blockchain.get("id") == blockchain_id:
                    return blockchain
            return None
        except Exception as e:
            self.logger.error(f"블록체인 정보 가져오기 실패: {str(e)}")
            return None
    
    def get_blockchain_transactions(self, blockchain_id: str, limit: int = 100) -> List[BlockchainTransaction]:
        """
        블록체인 트랜잭션 통계를 가져옵니다.
        
        Args:
            blockchain_id: 블록체인 ID
            limit: 반환할 항목 수
            
        Returns:
            List[BlockchainTransaction]: 블록체인 트랜잭션 통계 목록
        """
        try:
            # 실제 API 호출 대신 데모 데이터 생성
            now = datetime.now()
            data = []
            
            for i in range(limit):
                timestamp = now - timedelta(hours=i)
                
                # 블록체인별로 다른 패턴 생성
                if blockchain_id == "bitcoin":
                    tx_count = 3000 + random.randint(-300, 300)
                    avg_fee = 0.0001 + random.uniform(-0.00002, 0.00005)
                    block_size = 1.2 + random.uniform(-0.2, 0.3)
                elif blockchain_id == "ethereum":
                    tx_count = 15000 + random.randint(-1500, 1500)
                    avg_fee = 0.002 + random.uniform(-0.0005, 0.001)
                    block_size = 0.08 + random.uniform(-0.01, 0.02)
                elif blockchain_id == "solana":
                    tx_count = 50000 + random.randint(-5000, 5000)
                    avg_fee = 0.00001 + random.uniform(-0.000001, 0.000005)
                    block_size = 0.02 + random.uniform(-0.005, 0.005)
                else:
                    tx_count = 5000 + random.randint(-500, 500)
                    avg_fee = 0.0005 + random.uniform(-0.0001, 0.0001)
                    block_size = 0.5 + random.uniform(-0.1, 0.1)
                
                item = {
                    "blockchain_id": blockchain_id,
                    "timestamp": timestamp,
                    "tx_count": tx_count,
                    "avg_fee": avg_fee,
                    "block_size": block_size,
                    "active_addresses": int(tx_count * random.uniform(0.2, 0.4)),
                    "network_hashrate": random.uniform(100, 200) if blockchain_id == "bitcoin" else None
                }
                data.append(item)
            
            # BlockchainTransaction 객체로 변환하여 반환
            return [BlockchainTransaction.from_dict(item) for item in data]
        except Exception as e:
            self.logger.error(f"블록체인 트랜잭션 데이터 가져오기 실패: {str(e)}")
            return []
    
    def get_wallet_activities(self, blockchain_id: str, limit: int = 10) -> List[WalletActivity]:
        """
        지갑 활동 정보를 가져옵니다.
        
        Args:
            blockchain_id: 블록체인 ID
            limit: 반환할 항목 수
            
        Returns:
            List[WalletActivity]: 지갑 활동 정보 목록
        """
        try:
            # 실제 API 호출 대신 데모 데이터 생성
            now = datetime.now()
            
            # 블록체인별 지갑 주소 형식
            if blockchain_id == "bitcoin":
                prefix = "bc1"
            elif blockchain_id == "ethereum":
                prefix = "0x"
            elif blockchain_id == "solana":
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
                
                item = {
                    "blockchain_id": blockchain_id,
                    "address": address,
                    "timestamp": timestamp,
                    "amount": amount,
                    "direction": direction,
                    "transaction_hash": f"0x{''.join(random.choices('abcdef0123456789', k=64))}",
                    "activity_type": random.choice(["transfer", "swap", "stake", "unstake", "mint"])
                }
                data.append(item)
            
            # WalletActivity 객체로 변환하여 반환
            return [WalletActivity.from_dict(item) for item in data]
        except Exception as e:
            self.logger.error(f"지갑 활동 데이터 가져오기 실패: {str(e)}")
            return []
    
    def get_contract_activities(self, blockchain_id: str, limit: int = 100) -> List[ContractActivity]:
        """
        스마트 컨트랙트 활동 정보를 가져옵니다.
        
        Args:
            blockchain_id: 블록체인 ID
            limit: 반환할 항목 수
            
        Returns:
            List[ContractActivity]: 스마트 컨트랙트 활동 정보 목록
        """
        try:
            # 스마트 컨트랙트를 지원하지 않는 블록체인은 빈 목록 반환
            if blockchain_id not in ["ethereum", "solana", "cardano"]:
                return []
            
            # 실제 API 호출 대신 데모 데이터 생성
            now = datetime.now()
            
            data = []
            for i in range(limit):
                timestamp = now - timedelta(hours=i)
                
                if blockchain_id == "ethereum":
                    prefix = "0x"
                    activities = ["swap", "liquidity", "mint", "burn", "transfer"]
                elif blockchain_id == "solana":
                    prefix = "So1"
                    activities = ["swap", "liquidity", "stake", "unstake", "vote"]
                else:
                    prefix = "addr"
                    activities = ["transfer", "delegate", "vote", "claim"]
                
                contract_address = f"{prefix}{''.join(random.choices('abcdef0123456789', k=40))}"
                activity_type = random.choice(activities)
                volume = 10 ** random.uniform(2, 6)  # 100 ~ 1,000,000 범위
                
                item = {
                    "blockchain_id": blockchain_id,
                    "contract_address": contract_address,
                    "timestamp": timestamp,
                    "activity_type": activity_type,
                    "volume": volume,
                    "transaction_count": int(10 ** random.uniform(1, 3)),  # 10 ~ 1000 범위
                    "unique_users": int(10 ** random.uniform(0, 2))  # 1 ~ 100 범위
                }
                data.append(item)
            
            # ContractActivity 객체로 변환하여 반환
            return [ContractActivity.from_dict(item) for item in data]
        except Exception as e:
            self.logger.error(f"컨트랙트 활동 데이터 가져오기 실패: {str(e)}")
            return []
    
    def get_blocks(self, blockchain_id: str, limit: int = 10) -> List[Block]:
        """
        블록 정보를 가져옵니다.
        
        Args:
            blockchain_id: 블록체인 ID
            limit: 반환할 항목 수
            
        Returns:
            List[Block]: 블록 정보 목록
        """
        try:
            # 실제 API 호출 대신 데모 데이터 생성
            now = datetime.now()
            
            data = []
            blockchain_info = self.get_blockchain_by_id(blockchain_id)
            last_block = blockchain_info.get("last_block", 1000000) if blockchain_info else 1000000
            
            for i in range(limit):
                block_height = last_block - i
                timestamp = now - timedelta(minutes=i * 10)
                
                # 블록체인별 데이터 패턴
                if blockchain_id == "bitcoin":
                    tx_count = random.randint(1500, 3000)
                    size = random.uniform(0.8, 1.5)
                    miner = random.choice(["Binance Pool", "F2Pool", "Foundry USA", "AntPool", "ViaBTC"])
                    difficulty = 78349962886.63
                elif blockchain_id == "ethereum":
                    tx_count = random.randint(80, 150)
                    size = random.uniform(0.05, 0.1)
                    miner = random.choice(["Lido", "Coinbase", "Kraken", "Binance", "stakefish"])
                    difficulty = None
                else:
                    tx_count = random.randint(500, 5000)
                    size = random.uniform(0.1, 0.5)
                    miner = None
                    difficulty = None
                
                item = {
                    "blockchain_id": blockchain_id,
                    "height": block_height,
                    "hash": f"0x{''.join(random.choices('abcdef0123456789', k=64))}",
                    "timestamp": timestamp,
                    "transactions": tx_count,
                    "size": size,
                    "miner": miner,
                    "difficulty": difficulty
                }
                data.append(item)
            
            # Block 객체로 변환하여 반환
            return [Block.from_dict(item) for item in data]
        except Exception as e:
            self.logger.error(f"블록 데이터 가져오기 실패: {str(e)}")
            return []
    
    def get_blockchain_network_info(self, blockchain_id: str) -> Optional[BlockchainNetwork]:
        """
        블록체인 네트워크 정보를 가져옵니다.
        
        Args:
            blockchain_id: 블록체인 ID
            
        Returns:
            Optional[BlockchainNetwork]: 블록체인 네트워크 정보
        """
        try:
            # 실제 API 호출 대신 데모 데이터 생성
            if blockchain_id == "bitcoin":
                data = {
                    "blockchain_id": blockchain_id,
                    "node_count": random.randint(10000, 15000),
                    "average_block_time": 10.0,
                    "current_difficulty": 78349962886.63,
                    "hashrate": 450.0,
                    "staking_apy": None
                }
            elif blockchain_id == "ethereum":
                data = {
                    "blockchain_id": blockchain_id,
                    "node_count": random.randint(5000, 8000),
                    "average_block_time": 12.1,
                    "current_difficulty": 0.0,
                    "hashrate": None,
                    "staking_apy": 4.2
                }
            elif blockchain_id == "solana":
                data = {
                    "blockchain_id": blockchain_id,
                    "node_count": random.randint(1500, 3000),
                    "average_block_time": 0.4,
                    "current_difficulty": 0.0,
                    "hashrate": None,
                    "staking_apy": 6.1
                }
            elif blockchain_id == "cardano":
                data = {
                    "blockchain_id": blockchain_id,
                    "node_count": random.randint(3000, 5000),
                    "average_block_time": 20.0,
                    "current_difficulty": 0.0,
                    "hashrate": None,
                    "staking_apy": 3.5
                }
            else:
                return None
            
            # BlockchainNetwork 객체로 변환하여 반환
            return BlockchainNetwork.from_dict(data)
        except Exception as e:
            self.logger.error(f"블록체인 네트워크 정보 가져오기 실패: {str(e)}")
            return None 