from datetime import datetime, timedelta
from typing import Union, List, Dict, Any, Optional
import re

def format_number(value: Union[int, float], decimal_places: int = 2, thousand_separator: bool = True) -> str:
    """
    숫자를 읽기 쉬운 형식으로 포맷합니다.
    
    Args:
        value: 포맷할 숫자
        decimal_places: 소수점 자릿수
        thousand_separator: 천 단위 구분자 사용 여부
    
    Returns:
        str: 포맷된 숫자 문자열
    """
    if value is None:
        return "-"
    
    try:
        if isinstance(value, int) or value.is_integer():
            formatted = f"{int(value):,d}" if thousand_separator else str(int(value))
        else:
            formatted = f"{value:,.{decimal_places}f}" if thousand_separator else f"{value:.{decimal_places}f}"
        
        return formatted
    except (ValueError, TypeError, AttributeError):
        return str(value)

def format_currency(value: Union[int, float], currency: str = "₩", decimal_places: int = 0) -> str:
    """
    금액을 통화 형식으로 포맷합니다.
    
    Args:
        value: 포맷할 금액
        currency: 통화 기호
        decimal_places: 소수점 자릿수
    
    Returns:
        str: 포맷된 금액 문자열
    """
    if value is None:
        return "-"
    
    try:
        # 큰 금액은 K, M, B 단위로 표시
        if abs(value) >= 1_000_000_000:
            return f"{currency}{value/1_000_000_000:.{decimal_places}f}B"
        elif abs(value) >= 1_000_000:
            return f"{currency}{value/1_000_000:.{decimal_places}f}M"
        elif abs(value) >= 1_000:
            return f"{currency}{value/1_000:.{decimal_places}f}K"
        else:
            return f"{currency}{format_number(value, decimal_places)}"
    except (ValueError, TypeError):
        return f"{currency}{str(value)}"

def time_ago(dt: datetime, reference_dt: datetime = None) -> str:
    """
    주어진 날짜/시간이 얼마나 지났는지 표시합니다.
    
    Args:
        dt: 대상 날짜/시간
        reference_dt: 기준 날짜/시간 (None이면 현재 시간)
    
    Returns:
        str: 경과 시간 문자열 (예: "3분 전", "2시간 전")
    """
    if reference_dt is None:
        reference_dt = datetime.now()
    
    if not isinstance(dt, datetime):
        try:
            dt = datetime.fromisoformat(dt)
        except (ValueError, TypeError):
            return str(dt)
    
    diff = reference_dt - dt
    
    if diff.days < 0 or diff.seconds < 0:
        return f"{dt.strftime('%Y-%m-%d %H:%M')}"
    
    if diff.days > 365:
        years = diff.days // 365
        return f"{years}년 전"
    elif diff.days > 30:
        months = diff.days // 30
        return f"{months}개월 전"
    elif diff.days > 0:
        return f"{diff.days}일 전"
    elif diff.seconds >= 3600:
        hours = diff.seconds // 3600
        return f"{hours}시간 전"
    elif diff.seconds >= 60:
        minutes = diff.seconds // 60
        return f"{minutes}분 전"
    else:
        return "방금 전"

def shorten_address(address: str, chars: int = 4) -> str:
    """
    긴 주소(블록체인 주소 등)를 줄입니다.
    
    Args:
        address: 원본 주소
        chars: 앞뒤로 표시할 문자 수
    
    Returns:
        str: 줄인 주소 (예: "0x1234...5678")
    """
    if not address or len(address) <= chars * 2 + 3:
        return address
    
    return f"{address[:chars]}...{address[-chars:]}"

def parse_date_range(date_range: str) -> Dict[str, datetime]:
    """
    날짜 범위 문자열을 시작/종료 날짜로 파싱합니다.
    
    Args:
        date_range: 날짜 범위 문자열 (예: "최근 7일", "이번 달", "2023-01-01 ~ 2023-01-31")
    
    Returns:
        Dict[str, datetime]: 시작 및 종료 날짜가 포함된 딕셔너리
    """
    now = datetime.now()
    
    # 미리 정의된 범위
    if date_range == "오늘":
        start_date = now.replace(hour=0, minute=0, second=0, microsecond=0)
        end_date = now
    elif date_range == "어제":
        yesterday = now - timedelta(days=1)
        start_date = yesterday.replace(hour=0, minute=0, second=0, microsecond=0)
        end_date = yesterday.replace(hour=23, minute=59, second=59, microsecond=999999)
    elif date_range == "최근 7일":
        start_date = now - timedelta(days=7)
        end_date = now
    elif date_range == "최근 30일":
        start_date = now - timedelta(days=30)
        end_date = now
    elif date_range == "이번 달":
        start_date = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        end_date = now
    elif date_range == "지난 달":
        last_month = now.replace(day=1) - timedelta(days=1)
        start_date = last_month.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        end_date = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0) - timedelta(microseconds=1)
    else:
        # 직접 입력된 날짜 범위 구문 분석 시도
        pattern = r"(\d{4}-\d{2}-\d{2})\s*~\s*(\d{4}-\d{2}-\d{2})"
        match = re.match(pattern, date_range)
        
        if match:
            start_str, end_str = match.groups()
            try:
                start_date = datetime.fromisoformat(start_str)
                end_date = datetime.fromisoformat(end_str).replace(hour=23, minute=59, second=59, microsecond=999999)
            except ValueError:
                start_date = now - timedelta(days=30)
                end_date = now
        else:
            # 기본값: 최근 30일
            start_date = now - timedelta(days=30)
            end_date = now
    
    return {"start_date": start_date, "end_date": end_date}

def generate_random_color(index: int = None, opacity: float = 0.7) -> str:
    """
    시각화에 사용할 랜덤 색상을 생성합니다.
    
    Args:
        index: 색상 인덱스 (None이면 완전 랜덤)
        opacity: 투명도 (0.0 ~ 1.0)
    
    Returns:
        str: RGBA 색상 문자열
    """
    import random
    
    # 미리 정의된 색상 팔레트
    palettes = [
        [52, 152, 219],    # 파랑
        [46, 204, 113],    # 녹색
        [155, 89, 182],    # 보라
        [52, 73, 94],      # 진한 회색
        [231, 76, 60],     # 빨강
        [241, 196, 15],    # 노랑
        [230, 126, 34],    # 주황
        [26, 188, 156],    # 청록
        [149, 165, 166],   # 회색
        [211, 84, 0]       # 갈색
    ]
    
    if index is not None and index < len(palettes):
        color = palettes[index % len(palettes)]
    else:
        color = [random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)]
    
    return f"rgba({color[0]}, {color[1]}, {color[2]}, {opacity})"

def human_readable_size(size_bytes: int) -> str:
    """
    바이트 크기를 사람이 읽기 쉬운 형식으로 변환합니다.
    
    Args:
        size_bytes: 바이트 수
    
    Returns:
        str: 변환된 크기 (예: "1.23 MB")
    """
    if size_bytes < 0:
        raise ValueError("입력은 0 또는 양수여야 합니다")
    
    if size_bytes == 0:
        return "0 B"
    
    size_names = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
    i = 0
    
    while size_bytes >= 1024 and i < len(size_names) - 1:
        size_bytes /= 1024
        i += 1
    
    return f"{size_bytes:.2f} {size_names[i]}" 