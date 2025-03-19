import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional, Union, Tuple
import random

def generate_blockchain_trend(
    blockchain_id: str,
    days: int = 30,
    seed: Optional[int] = None
) -> pd.DataFrame:
    """
    블록체인 트랜드 데이터를 생성합니다.
    
    Args:
        blockchain_id: 블록체인 ID
        days: 생성할 일수
        seed: 난수 시드 (재현 가능성을 위함)
        
    Returns:
        pd.DataFrame: 생성된 트랜드 데이터
    """
    if seed is not None:
        random.seed(seed)
        np.random.seed(seed)
    
    now = datetime.now()
    dates = [now - timedelta(days=i) for i in range(days)]
    dates.reverse()  # 시간순 정렬
    
    # 블록체인별 기본 값 설정
    if blockchain_id == "bitcoin":
        base_tx_count = 300000
        tx_volatility = 0.1
        base_active_addresses = 1000000
        address_volatility = 0.15
        base_fee = 0.0001
        fee_volatility = 0.3
    elif blockchain_id == "ethereum":
        base_tx_count = 1200000
        tx_volatility = 0.15
        base_active_addresses = 500000
        address_volatility = 0.12
        base_fee = 0.002
        fee_volatility = 0.4
    elif blockchain_id == "solana":
        base_tx_count = 2000000
        tx_volatility = 0.2
        base_active_addresses = 300000
        address_volatility = 0.1
        base_fee = 0.00001
        fee_volatility = 0.1
    else:
        base_tx_count = 500000
        tx_volatility = 0.12
        base_active_addresses = 200000
        address_volatility = 0.1
        base_fee = 0.0005
        fee_volatility = 0.2
    
    # 약간의 트랜드 추가 (시간이 지남에 따라 증가)
    trend_factor = np.linspace(0.8, 1.2, days)
    
    # 데이터 생성
    data = []
    for i, date in enumerate(dates):
        # 요일에 따른 변동 (주말에는 약간 감소)
        weekday_factor = 0.9 if date.weekday() >= 5 else 1.0
        
        # 기본값에 변동성과 트랜드 적용
        tx_count = int(base_tx_count * trend_factor[i] * weekday_factor * 
                      (1 + np.random.normal(0, tx_volatility)))
        active_addresses = int(base_active_addresses * trend_factor[i] * weekday_factor * 
                             (1 + np.random.normal(0, address_volatility)))
        avg_fee = base_fee * (1 + np.random.normal(0, fee_volatility))
        
        # 과도한 변동 방지
        tx_count = max(tx_count, int(base_tx_count * 0.5))
        active_addresses = max(active_addresses, int(base_active_addresses * 0.5))
        avg_fee = max(avg_fee, base_fee * 0.3)
        
        data.append({
            "date": date.date(),
            "blockchain_id": blockchain_id,
            "tx_count": tx_count,
            "active_addresses": active_addresses,
            "avg_fee": avg_fee
        })
    
    return pd.DataFrame(data)

def calculate_stats(df: pd.DataFrame, column: str) -> Dict[str, float]:
    """
    데이터프레임의 특정 컬럼에 대한 통계를 계산합니다.
    
    Args:
        df: 데이터프레임
        column: 통계를 계산할 컬럼명
        
    Returns:
        Dict[str, float]: 통계 결과
    """
    return {
        "mean": df[column].mean(),
        "median": df[column].median(),
        "std": df[column].std(),
        "min": df[column].min(),
        "max": df[column].max(),
        "q25": df[column].quantile(0.25),
        "q75": df[column].quantile(0.75)
    }

def calculate_change(
    df: pd.DataFrame, 
    column: str, 
    periods: List[int] = [1, 7, 30]
) -> Dict[str, float]:
    """
    데이터프레임의 특정 컬럼에 대한 변화율을 계산합니다.
    
    Args:
        df: 데이터프레임 (날짜로 정렬되어 있어야 함)
        column: 변화율을 계산할 컬럼명
        periods: 계산할 기간 목록 (일)
        
    Returns:
        Dict[str, float]: 기간별 변화율
    """
    changes = {}
    
    if len(df) == 0:
        return changes
    
    latest_value = df[column].iloc[-1]
    
    for period in periods:
        if len(df) > period:
            previous_value = df[column].iloc[-(period+1)]
            if previous_value != 0:
                change_pct = (latest_value - previous_value) / previous_value * 100
                changes[f"{period}d"] = change_pct
    
    return changes

def forecast_blockchain_activity(
    df: pd.DataFrame,
    days_ahead: int = 7,
    smoothing_factor: float = 0.3
) -> pd.DataFrame:
    """
    블록체인 활동을 간단히 예측합니다.
    
    Args:
        df: 과거 데이터 (날짜로 정렬된 데이터프레임)
        days_ahead: 예측할 일수
        smoothing_factor: 지수 평활 계수 (0~1)
        
    Returns:
        pd.DataFrame: 예측 데이터
    """
    if len(df) < 7:
        raise ValueError("예측을 위해서는 최소 7일 이상의 데이터가 필요합니다.")
    
    # 마지막 날짜
    last_date = df["date"].iloc[-1]
    
    # 예측 기간 생성
    forecast_dates = [last_date + timedelta(days=i+1) for i in range(days_ahead)]
    
    # 간단한 지수 평활 예측 구현
    numeric_columns = ["tx_count", "active_addresses", "avg_fee"]
    forecast_data = []
    
    for i, date in enumerate(forecast_dates):
        forecast_row = {"date": date, "blockchain_id": df["blockchain_id"].iloc[0], "is_forecast": True}
        
        for col in numeric_columns:
            if i == 0:
                # 첫 번째 예측은 최근 7일 평균과 가장 최근 값의 가중 평균
                last_value = df[col].iloc[-1]
                week_avg = df[col].iloc[-7:].mean()
                forecast_value = last_value * (1 - smoothing_factor) + week_avg * smoothing_factor
            else:
                # 이후 예측은 이전 예측과 전체 트랜드의 가중 평균
                last_forecast = forecast_data[i-1][col]
                trend = (df[col].iloc[-1] - df[col].iloc[0]) / len(df)
                forecast_value = last_forecast + trend * smoothing_factor
            
            # 약간의 랜덤성 추가
            noise = np.random.normal(0, 0.03)
            forecast_value = forecast_value * (1 + noise)
            
            # 음수 방지
            forecast_value = max(forecast_value, 0)
            
            forecast_row[col] = forecast_value
        
        forecast_data.append(forecast_row)
    
    # 예측 데이터프레임 생성
    forecast_df = pd.DataFrame(forecast_data)
    
    # 원본 데이터에 is_forecast 컬럼 추가
    df_with_flag = df.copy()
    df_with_flag["is_forecast"] = False
    
    # 결합
    result = pd.concat([df_with_flag, forecast_df], ignore_index=True)
    
    return result

def categorize_blockchain_activity(value: float, blockchain_id: str, metric: str) -> str:
    """
    블록체인 활동 지표를 범주화합니다.
    
    Args:
        value: 활동 값
        blockchain_id: 블록체인 ID
        metric: 지표 유형 ('tx_count', 'active_addresses', 'avg_fee' 등)
        
    Returns:
        str: 범주 ('very_low', 'low', 'medium', 'high', 'very_high')
    """
    # 블록체인별, 지표별 임계값 설정
    thresholds = {
        "bitcoin": {
            "tx_count": [200000, 250000, 350000, 400000],
            "active_addresses": [800000, 900000, 1100000, 1200000],
            "avg_fee": [0.00005, 0.0001, 0.0002, 0.0005]
        },
        "ethereum": {
            "tx_count": [900000, 1000000, 1400000, 1600000],
            "active_addresses": [400000, 450000, 550000, 600000],
            "avg_fee": [0.001, 0.0015, 0.003, 0.005]
        },
        "solana": {
            "tx_count": [1500000, 1800000, 2200000, 2500000],
            "active_addresses": [200000, 250000, 350000, 400000],
            "avg_fee": [0.000005, 0.00001, 0.00002, 0.00005]
        }
    }
    
    # 기본 임계값 (다른 블록체인용)
    default_thresholds = {
        "tx_count": [400000, 450000, 550000, 600000],
        "active_addresses": [150000, 180000, 220000, 250000],
        "avg_fee": [0.0003, 0.0004, 0.0006, 0.0008]
    }
    
    # 해당 블록체인 임계값 가져오기
    chain_thresholds = thresholds.get(blockchain_id, default_thresholds)
    metric_thresholds = chain_thresholds.get(metric, default_thresholds[metric])
    
    # 범주 결정
    if value < metric_thresholds[0]:
        return "very_low"
    elif value < metric_thresholds[1]:
        return "low"
    elif value < metric_thresholds[2]:
        return "medium"
    elif value < metric_thresholds[3]:
        return "high"
    else:
        return "very_high"

def wallet_risk_score(transactions: List[Dict[str, Any]]) -> float:
    """
    지갑의 위험 점수를 계산합니다.
    
    Args:
        transactions: 지갑 트랜잭션 목록
        
    Returns:
        float: 위험 점수 (0~100)
    """
    if not transactions:
        return 0
    
    # 위험 요소들
    risk_factors = {
        "recent_activity": 0,  # 최근 활동 빈도
        "volume": 0,           # 거래량
        "age": 0,              # 계정 나이
        "pattern": 0,          # 거래 패턴
        "connections": 0       # 연결된 주소
    }
    
    # 최근 활동 분석
    now = datetime.now()
    timestamps = [tx.get("timestamp") for tx in transactions if tx.get("timestamp")]
    if timestamps:
        latest = max(timestamps)
        if isinstance(latest, str):
            latest = datetime.fromisoformat(latest.replace('Z', '+00:00'))
        days_since_last = (now - latest).days
        
        if days_since_last < 1:
            risk_factors["recent_activity"] = 25  # 24시간 내 활동
        elif days_since_last < 7:
            risk_factors["recent_activity"] = 15  # 일주일 내 활동
        elif days_since_last < 30:
            risk_factors["recent_activity"] = 10  # 한 달 내 활동
        else:
            risk_factors["recent_activity"] = 5   # 오래된 활동
    
    # 거래량 분석
    volumes = [tx.get("amount", 0) for tx in transactions]
    if volumes:
        avg_volume = sum(volumes) / len(volumes)
        max_volume = max(volumes)
        
        if max_volume > 10000:
            risk_factors["volume"] = 25
        elif max_volume > 1000:
            risk_factors["volume"] = 15
        elif max_volume > 100:
            risk_factors["volume"] = 10
        else:
            risk_factors["volume"] = 5
    
    # 계정 나이
    if timestamps:
        first = min(timestamps)
        if isinstance(first, str):
            first = datetime.fromisoformat(first.replace('Z', '+00:00'))
        account_age_days = (now - first).days
        
        if account_age_days < 7:
            risk_factors["age"] = 20  # 일주일 미만의 신규 계정
        elif account_age_days < 30:
            risk_factors["age"] = 15  # 한 달 미만
        elif account_age_days < 180:
            risk_factors["age"] = 10  # 6개월 미만
        else:
            risk_factors["age"] = 5   # 오래된 계정
    
    # 거래 패턴 분석 (방향 패턴)
    directions = [tx.get("direction") for tx in transactions if tx.get("direction")]
    if len(directions) >= 3:
        # 입출금 반복 패턴 확인
        pattern_score = 0
        for i in range(1, len(directions)):
            if directions[i] != directions[i-1]:
                pattern_score += 1
        
        pattern_ratio = pattern_score / (len(directions) - 1)
        risk_factors["pattern"] = int(pattern_ratio * 15)
    
    # 연결된 주소 수
    connected_addresses = set()
    for tx in transactions:
        to_addr = tx.get("to_address")
        from_addr = tx.get("from_address")
        
        if to_addr:
            connected_addresses.add(to_addr)
        if from_addr:
            connected_addresses.add(from_addr)
    
    conn_count = len(connected_addresses)
    if conn_count > 20:
        risk_factors["connections"] = 15
    elif conn_count > 10:
        risk_factors["connections"] = 10
    elif conn_count > 5:
        risk_factors["connections"] = 5
    else:
        risk_factors["connections"] = 3
    
    # 총점 계산
    total_score = sum(risk_factors.values())
    
    return min(total_score, 100)  # 최대 100점으로 제한 