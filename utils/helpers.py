import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import json
import yaml
import os
from typing import Dict, List, Any, Optional, Tuple, Union

def load_config(config_path: str) -> Dict[str, Any]:
    """
    YAML 설정 파일을 로드합니다.
    
    Args:
        config_path: 설정 파일 경로
    
    Returns:
        설정 정보가 담긴 딕셔너리
    """
    try:
        with open(config_path, 'r') as file:
            config = yaml.safe_load(file)
        return config
    except Exception as e:
        print(f"설정 파일 로드 오류: {str(e)}")
        return {}

def save_config(config: Dict[str, Any], config_path: str) -> bool:
    """
    설정을 YAML 파일로 저장합니다.
    
    Args:
        config: 설정 딕셔너리
        config_path: 저장할 파일 경로
    
    Returns:
        성공 여부
    """
    try:
        with open(config_path, 'w') as file:
            yaml.dump(config, file, default_flow_style=False)
        return True
    except Exception as e:
        print(f"설정 파일 저장 오류: {str(e)}")
        return False

def parse_iso_datetime(dt_str: str) -> datetime:
    """
    ISO 형식의 날짜/시간 문자열을 datetime 객체로 변환합니다.
    
    Args:
        dt_str: ISO 형식 날짜/시간 문자열 (예: '2023-06-10T15:30:45Z')
    
    Returns:
        datetime 객체
    """
    return datetime.fromisoformat(dt_str.replace('Z', '+00:00'))

def format_datetime(dt: datetime, format_str: str = "%Y-%m-%d %H:%M:%S") -> str:
    """
    datetime 객체를 지정된 형식의 문자열로 변환합니다.
    
    Args:
        dt: datetime 객체
        format_str: 날짜/시간 형식 문자열
    
    Returns:
        형식화된 날짜/시간 문자열
    """
    return dt.strftime(format_str)

def format_number(value: float, decimal_places: int = 2, use_thousands_separator: bool = True) -> str:
    """
    숫자를 읽기 쉬운 형식으로 변환합니다.
    
    Args:
        value: 형식화할 숫자
        decimal_places: 소수점 자릿수
        use_thousands_separator: 천 단위 구분자 사용 여부
    
    Returns:
        형식화된 숫자 문자열
    """
    if use_thousands_separator:
        return f"{value:,.{decimal_places}f}"
    else:
        return f"{value:.{decimal_places}f}"

def format_percentage(value: float, decimal_places: int = 2) -> str:
    """
    값을 백분율로 변환합니다.
    
    Args:
        value: 변환할 값 (0.1 = 10%)
        decimal_places: 소수점 자릿수
    
    Returns:
        백분율 문자열
    """
    return f"{value * 100:.{decimal_places}f}%"

def format_currency(value: float, currency: str = "USD", decimal_places: int = 2) -> str:
    """
    화폐 값을 형식화합니다.
    
    Args:
        value: 금액
        currency: 통화 (USD, KRW, BTC 등)
        decimal_places: 소수점 자릿수
    
    Returns:
        형식화된 통화 문자열
    """
    currency_symbols = {
        "USD": "$",
        "KRW": "₩",
        "EUR": "€",
        "JPY": "¥",
        "GBP": "£",
        "BTC": "₿",
        "ETH": "Ξ"
    }
    
    symbol = currency_symbols.get(currency, currency)
    
    # 암호화폐의 경우 소수점 더 많이 표시
    if currency in ["BTC", "ETH"]:
        decimal_places = max(decimal_places, 8)
    
    # 통화별 형식 처리 (천단위 구분, 소수점 등)
    if currency in ["KRW", "JPY"]:  # 소수점 없는 통화
        return f"{symbol}{value:,.0f}"
    else:
        return f"{symbol}{value:,.{decimal_places}f}"

def time_ago(dt: datetime) -> str:
    """
    주어진 시간이 얼마나 지났는지 표시합니다.
    
    Args:
        dt: 비교할 datetime 객체
    
    Returns:
        "n분 전", "n시간 전" 등의 문자열
    """
    now = datetime.now()
    delta = now - dt
    
    if delta.days > 365:
        years = delta.days // 365
        return f"{years}년 전"
    elif delta.days > 30:
        months = delta.days // 30
        return f"{months}개월 전"
    elif delta.days > 0:
        return f"{delta.days}일 전"
    elif delta.seconds >= 3600:
        hours = delta.seconds // 3600
        return f"{hours}시간 전"
    elif delta.seconds >= 60:
        minutes = delta.seconds // 60
        return f"{minutes}분 전"
    else:
        return f"{delta.seconds}초 전"

def generate_date_range(start_date: Union[str, datetime], end_date: Union[str, datetime], 
                         freq: str = 'D') -> List[datetime]:
    """
    날짜 범위를 생성합니다.
    
    Args:
        start_date: 시작 날짜 (문자열 또는 datetime)
        end_date: 종료 날짜 (문자열 또는 datetime)
        freq: 주기 ('D'=일별, 'W'=주별, 'M'=월별, 'H'=시간별)
    
    Returns:
        datetime 객체 리스트
    """
    # 문자열을 datetime으로 변환
    if isinstance(start_date, str):
        start_date = parse_iso_datetime(start_date)
    if isinstance(end_date, str):
        end_date = parse_iso_datetime(end_date)
    
    # pandas 날짜 범위 생성 후 리스트로 변환
    date_range = pd.date_range(start=start_date, end=end_date, freq=freq)
    return date_range.tolist()

def calculate_percentage_change(old_value: float, new_value: float) -> float:
    """
    두 값 사이의 백분율 변화를 계산합니다.
    
    Args:
        old_value: 이전 값
        new_value: 새 값
    
    Returns:
        백분율 변화 (예: 0.1 = 10% 증가)
    """
    if old_value == 0:
        return float('inf') if new_value > 0 else float('-inf') if new_value < 0 else 0
    
    return (new_value - old_value) / abs(old_value)

def calculate_moving_average(data: List[float], window: int = 7) -> List[float]:
    """
    이동 평균을 계산합니다.
    
    Args:
        data: 값 리스트
        window: 이동 평균 기간
    
    Returns:
        이동 평균 리스트
    """
    if len(data) < window:
        return [sum(data) / len(data)] * len(data)
    
    result = []
    for i in range(len(data)):
        if i < window - 1:
            # 기간이 충분하지 않은 경우 앞부분 채우기
            result.append(sum(data[:i+1]) / (i+1))
        else:
            result.append(sum(data[i-window+1:i+1]) / window)
    
    return result

def is_valid_json(json_str: str) -> bool:
    """
    문자열이 유효한 JSON인지 확인합니다.
    
    Args:
        json_str: 검사할 JSON 문자열
    
    Returns:
        유효성 여부
    """
    try:
        json.loads(json_str)
        return True
    except ValueError:
        return False

def create_directory_if_not_exists(directory_path: str) -> bool:
    """
    디렉토리가 없으면 생성합니다.
    
    Args:
        directory_path: 생성할 디렉토리 경로
    
    Returns:
        성공 여부
    """
    if not os.path.exists(directory_path):
        try:
            os.makedirs(directory_path)
            return True
        except Exception as e:
            print(f"디렉토리 생성 오류: {str(e)}")
            return False
    return True 