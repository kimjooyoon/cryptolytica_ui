import streamlit as st
import pandas as pd
import sys
import os
from datetime import datetime, timedelta
import random
from pathlib import Path

# 상위 디렉토리 경로 추가
ROOT_DIR = Path(__file__).parent.parent.parent.parent
sys.path.append(str(ROOT_DIR))

from shared.services.base_client import BaseApiClient
from domains.exchange.services.exchange_client import ExchangeClient
from domains.blockchain.services.blockchain_client import BlockchainClient
from domains.market.services.market_client import MarketClient
from shared.utils.visualization import create_gauge_chart, create_line_chart, create_pie_chart
from shared.utils.helpers import format_percentage, format_currency, time_ago
from core.config import get_config_value
from core.state import get_domain_state, set_domain_state

# 페이지 타이틀
page_title = "대시보드"

def render_page():
    """대시보드 페이지를 렌더링합니다."""
    
    # 사이드바 제목
    st.sidebar.title("대시보드")
    
    # API 클라이언트 생성
    exchange_client = get_exchange_client()
    blockchain_client = get_blockchain_client()
    market_client = get_market_client()
    
    # 시스템 상태 가져오기
    system_status = get_system_status()
    
    # 거래소 목록 가져오기
    exchanges = get_exchanges(exchange_client)
    
    # 블록체인 목록 가져오기
    blockchains = get_blockchains(blockchain_client)
    
    # 페이지 헤더
    st.title("CryptoLytica 대시보드")
    st.markdown("암호화폐 데이터 분석 시스템의 상태와 주요 지표를 확인합니다.")

    # 상태 카드
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="시스템 상태",
            value=system_status.status,
            delta="정상" if system_status.status == "running" else "주의 필요"
        )
    
    with col2:
        st.metric(
            label="데이터 수집기",
            value=f"{list(system_status.collectors.values()).count('running')}/{len(system_status.collectors)}",
            delta="모두 정상" if all(status == "running" for status in system_status.collectors.values()) else "일부 문제"
        )
    
    with col3:
        st.metric(
            label="CPU 사용률",
            value=f"{system_status.cpu_usage:.1f}%",
            delta=f"{-5:.1f}%" if system_status.cpu_usage < 50 else f"{5:.1f}%",
            delta_color="inverse"
        )
    
    with col4:
        st.metric(
            label="메모리 사용률",
            value=f"{system_status.memory_usage:.1f}%",
            delta=f"{-3:.1f}%" if system_status.memory_usage < 60 else f"{3:.1f}%",
            delta_color="inverse"
        )
    
    # 나머지 대시보드 구현...
    
    # 이벤트 목록
    st.header("최근 시스템 이벤트")
    events = get_events()
    
    if events:
        df_events = pd.DataFrame(events[:10])
        df_events['상태'] = df_events['status']
        df_events['시간'] = df_events['timestamp'].apply(lambda x: time_ago(datetime.fromisoformat(x)))
        df_events['이벤트'] = df_events['event']
        
        # 상태에 따라 색상 스타일 적용
        def highlight_status(val):
            if val == '성공':
                return 'background-color: #aaffaa'
            elif val == '경고':
                return 'background-color: #ffddaa'
            elif val == '오류':
                return 'background-color: #ffaaaa'
            return ''
        
        st.dataframe(
            df_events[['이벤트', '시간', '상태']],
            hide_index=True,
            use_container_width=True,
            column_config={
                "이벤트": st.column_config.TextColumn(
                    "이벤트 설명",
                    width="large"
                ),
                "시간": st.column_config.TextColumn(
                    "발생 시간",
                    width="small"
                ),
                "상태": st.column_config.TextColumn(
                    "상태",
                    width="small"
                )
            }
        )
    else:
        st.info("표시할 이벤트가 없습니다.")
    
    # 자산 분포도
    st.header("암호화폐 자산 분포")
    asset_distribution = get_asset_distribution()
    
    if not asset_distribution.empty:
        fig = create_pie_chart(
            asset_distribution,
            values_col='value',
            names_col='asset',
            title='암호화폐 자산 분포'
        )
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("자산 데이터를 불러올 수 없습니다.")
    
    # 상태 저장
    set_domain_state('dashboard', 'last_refresh', datetime.now().isoformat())

# API 클라이언트 생성
@st.cache_resource
def get_exchange_client():
    base_url = get_config_value('api.base_url', 'http://localhost:8000')
    api_key = get_config_value('api.api_key', '')
    ws_url = get_config_value('api.ws_url', '')
    return ExchangeClient(base_url=base_url, api_key=api_key, ws_url=ws_url)

@st.cache_resource
def get_blockchain_client():
    base_url = get_config_value('api.base_url', 'http://localhost:8000')
    api_key = get_config_value('api.api_key', '')
    ws_url = get_config_value('api.ws_url', '')
    return BlockchainClient(base_url=base_url, api_key=api_key, ws_url=ws_url)

@st.cache_resource
def get_market_client():
    base_url = get_config_value('api.base_url', 'http://localhost:8000')
    api_key = get_config_value('api.api_key', '')
    ws_url = get_config_value('api.ws_url', '')
    return MarketClient(base_url=base_url, api_key=api_key, ws_url=ws_url)

# 시스템 상태 가져오기
@st.cache_data(ttl=60)
def get_system_status():
    # 데모용 가상 데이터 생성
    data = {
        "status": "running",
        "version": "1.0.0",
        "uptime": "5d 12h 30m",
        "collectors": {
            "exchange": "running",
            "blockchain": "running"
        },
        "processors": {
            "market": "running",
            "portfolio": "running"
        },
        "database": {
            "status": "connected",
            "size": "1.2 GB"
        },
        "cpu_usage": 32.5,
        "memory_usage": 42.8,
        "disk_usage": 68.3,
        "last_update": datetime.now().isoformat()
    }
    
    from shared.models.common_models import SystemStatus
    return SystemStatus.from_dict(data)

# 거래소 목록 가져오기
@st.cache_data(ttl=300)
def get_exchanges(client):
    return client.get_exchanges()

# 블록체인 목록 가져오기
@st.cache_data(ttl=300)
def get_blockchains(client):
    return client.get_blockchains()

# 이벤트 가져오기 (가상 데이터)
@st.cache_data(ttl=120)
def get_events(limit=10):
    now = datetime.now()
    events = [
        {
            "id": "evt1",
            "timestamp": (now - timedelta(minutes=15)).isoformat(),
            "event": "바이낸스 데이터 수집 완료",
            "status": "성공"
        },
        {
            "id": "evt2",
            "timestamp": (now - timedelta(minutes=35)).isoformat(),
            "event": "BTC 온체인 분석 업데이트",
            "status": "성공"
        },
        {
            "id": "evt3",
            "timestamp": (now - timedelta(minutes=50)).isoformat(),
            "event": "시스템 백업 완료",
            "status": "성공"
        },
        {
            "id": "evt4",
            "timestamp": (now - timedelta(hours=2)).isoformat(),
            "event": "Upbit API 연결 문제 해결됨",
            "status": "경고"
        },
        {
            "id": "evt5",
            "timestamp": (now - timedelta(hours=3)).isoformat(),
            "event": "이더리움 데이터 피드 재시작",
            "status": "성공"
        }
    ]
    
    return events[:limit]

# 자산 분포 가져오기 (가상 데이터)
@st.cache_data(ttl=600)
def get_asset_distribution():
    data = [
        {"asset": "Bitcoin", "value": 45.2},
        {"asset": "Ethereum", "value": 32.1},
        {"asset": "Solana", "value": 12.5},
        {"asset": "Cardano", "value": 6.8},
        {"asset": "기타", "value": 3.4}
    ]
    
    return pd.DataFrame(data) 