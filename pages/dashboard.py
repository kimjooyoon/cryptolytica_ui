import streamlit as st
import pandas as pd
import sys
import os
from datetime import datetime, timedelta
import random

# 상위 디렉토리 추가하여 api 모듈을 import할 수 있도록 함
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from api.client import CryptoLyticaClient
from utils.visualization import create_gauge_chart, create_line_chart, create_pie_chart
from utils.helpers import format_percentage, format_currency, time_ago

# 페이지 설정
st.set_page_config(
    page_title="CryptoLytica - 대시보드",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 사이드바 제목
st.sidebar.title("대시보드")

# 설정 로드
@st.cache_data(ttl=300)
def load_config():
    import yaml
    try:
        with open('config/config.yaml', 'r') as file:
            return yaml.safe_load(file)
    except FileNotFoundError:
        st.error("config/config.yaml 파일을 찾을 수 없습니다.")
        return {}

config = load_config()

# API 클라이언트 생성
@st.cache_resource
def get_api_client():
    api_config = config.get('api', {})
    return CryptoLyticaClient(
        base_url=api_config.get('base_url', 'http://localhost:8000'),
        api_key=api_config.get('api_key', ''),
        ws_url=api_config.get('ws_url', '')
    )

client = get_api_client()

# 시스템 상태 가져오기
@st.cache_data(ttl=60)
def get_system_status():
    return client.get_system_status()

# 거래소 목록 가져오기
@st.cache_data(ttl=300)
def get_exchanges():
    return client.get_exchanges()

# 블록체인 목록 가져오기
@st.cache_data(ttl=300)
def get_blockchains():
    return client.get_blockchains()

# 시스템 로드 가져오기 (가상 데이터)
@st.cache_data(ttl=60)
def get_system_load():
    # 가상 시계열 데이터 생성
    end_time = datetime.now()
    start_time = end_time - timedelta(hours=24)
    
    times = []
    cpu_values = []
    memory_values = []
    api_requests = []
    
    current_time = start_time
    while current_time <= end_time:
        times.append(current_time)
        
        # 시간에 따른 패턴 생성
        hour = current_time.hour
        base_cpu = 30 + (hour % 12) * 5  # 시간에 따라 변동
        base_memory = 40 + (hour % 8) * 5  # 시간에 따라 변동
        base_api = 100 + hour * 20  # 시간에 따라 트래픽 증가
        
        # 약간의 무작위성 추가
        cpu_values.append(base_cpu + random.uniform(-5, 5))
        memory_values.append(base_memory + random.uniform(-3, 3))
        api_requests.append(base_api + random.uniform(-20, 20))
        
        current_time += timedelta(hours=1)
    
    return pd.DataFrame({
        'timestamp': times,
        'CPU 사용률': cpu_values,
        '메모리 사용률': memory_values,
        'API 요청': api_requests
    })

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
        },
        {
            "id": "evt6",
            "timestamp": (now - timedelta(hours=4)).isoformat(),
            "event": "시스템 메모리 부족 경고",
            "status": "경고"
        },
        {
            "id": "evt7", 
            "timestamp": (now - timedelta(hours=5)).isoformat(),
            "event": "데이터베이스 백업 완료",
            "status": "성공"
        },
        {
            "id": "evt8",
            "timestamp": (now - timedelta(hours=6)).isoformat(),
            "event": "코인베이스 API 할당량 80% 도달",
            "status": "정보"
        }
    ]
    return events[:limit]

# 자산 분포 가져오기 (가상 데이터)
@st.cache_data(ttl=600)
def get_asset_distribution():
    return {
        "labels": ["Bitcoin", "Ethereum", "Solana", "Cardano", "기타"],
        "values": [45, 30, 10, 8, 7]
    }

# 페이지 타이틀
st.title("CryptoLytica 대시보드")

# 새로고침 버튼
if st.button("새로고침"):
    st.cache_data.clear()
    st.experimental_rerun()

# 날짜 범위 선택기
st.sidebar.date_input(
    "날짜 선택",
    value=datetime.now(),
    disabled=True,  # 실제 기능은 아직 구현하지 않음
    help="데이터 표시 날짜 (현재는 비활성화 상태)"
)

# 새로고침 간격 선택
refresh_interval = st.sidebar.selectbox(
    "자동 새로고침 간격",
    options=[0, 30, 60, 300, 600],
    format_func=lambda x: "사용 안함" if x == 0 else f"{x}초",
    index=1
)

if refresh_interval > 0:
    st.sidebar.info(f"{refresh_interval}초마다 자동 새로고침됩니다.")

# 메인 컨텐츠
try:
    system_status = get_system_status()
    
    # 상태 카드
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.subheader("시스템 상태")
        st.metric(
            label="API 서버",
            value=system_status.get("status", "offline"),
            delta="정상" if system_status.get("status") == "online" else "오프라인"
        )
        st.metric(
            label="가동 시간",
            value=system_status.get("uptime", "N/A")
        )
        st.metric(
            label="버전",
            value=system_status.get("version", "N/A")
        )
    
    with col2:
        st.subheader("컬렉터 상태")
        collectors = system_status.get("collectors", {})
        st.metric(
            label="거래소 데이터 수집기",
            value=collectors.get("exchange", "중지됨"),
            delta="실행 중" if collectors.get("exchange") == "running" else "중지됨"
        )
        st.metric(
            label="블록체인 데이터 수집기",
            value=collectors.get("blockchain", "중지됨"),
            delta="실행 중" if collectors.get("blockchain") == "running" else "중지됨"
        )
    
    with col3:
        st.subheader("프로세서 상태")
        processors = system_status.get("processors", {})
        st.metric(
            label="시장 분석",
            value=processors.get("market", "중지됨"),
            delta="실행 중" if processors.get("market") == "running" else "중지됨"
        )
        st.metric(
            label="데이터 분석",
            value=processors.get("analytics", "중지됨"),
            delta="실행 중" if processors.get("analytics") == "running" else "중지됨"
        )
    
    # 시스템 로드 그래프
    st.subheader("시스템 로드")
    system_load = get_system_load()
    
    # 차트 생성
    st.plotly_chart(
        create_line_chart(
            system_load, 
            'timestamp', 
            ['CPU 사용률', '메모리 사용률'], 
            title="시스템 리소스 사용률 (24시간)"
        ),
        use_container_width=True
    )
    
    st.plotly_chart(
        create_line_chart(
            system_load, 
            'timestamp', 
            ['API 요청'], 
            title="API 요청 수 (24시간)"
        ),
        use_container_width=True
    )
    
    # 거래소 및 블록체인 상태
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("연결된 거래소")
        exchanges = get_exchanges()
        
        if exchanges:
            exchanges_df = pd.DataFrame(exchanges)
            st.dataframe(
                exchanges_df[['name', 'status', 'last_update']],
                hide_index=True,
                use_container_width=True
            )
        else:
            st.info("연결된 거래소가 없습니다.")
    
    with col2:
        st.subheader("연결된 블록체인")
        blockchains = get_blockchains()
        
        if blockchains:
            blockchains_df = pd.DataFrame(blockchains)
            st.dataframe(
                blockchains_df[['name', 'status', 'last_block', 'last_update']],
                hide_index=True,
                use_container_width=True
            )
        else:
            st.info("연결된 블록체인이 없습니다.")
    
    # 자산 분포 및 디스크 사용량
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("자산 분포")
        asset_distribution = get_asset_distribution()
        
        st.plotly_chart(
            create_pie_chart(
                asset_distribution["labels"],
                asset_distribution["values"],
                title="암호화폐 별 자산 분포"
            ),
            use_container_width=True
        )
    
    with col2:
        st.subheader("디스크 사용량")
        database = system_status.get("database", {})
        
        # 게이지 차트 생성
        storage_used = 250  # GB
        storage_total = 500  # GB
        storage_percent = storage_used / storage_total
        
        st.plotly_chart(
            create_gauge_chart(
                storage_percent,
                0,
                1,
                title=f"디스크 사용량: {storage_used}GB / {storage_total}GB",
                threshold_values=[0.6, 0.8]
            ),
            use_container_width=True
        )
    
    # 최근 이벤트
    st.subheader("최근 이벤트")
    events = get_events()
    
    if events:
        # 타임스탬프를 "n시간 전" 형식으로 변환
        for event in events:
            event_time = datetime.fromisoformat(event["timestamp"].replace('Z', '+00:00'))
            event["time_ago"] = time_ago(event_time)
        
        events_df = pd.DataFrame(events)
        
        # 상태에 따라 색상 적용
        def highlight_status(val):
            if val == "성공":
                return 'background-color: #c6efce; color: #006100'
            elif val == "경고":
                return 'background-color: #ffeb9c; color: #9c5700'
            elif val == "오류":
                return 'background-color: #ffc7ce; color: #9c0006'
            return ''
        
        # 스타일 적용된 데이터프레임 표시
        styled_df = events_df[['time_ago', 'event', 'status']].style.applymap(
            highlight_status, subset=['status']
        )
        
        st.dataframe(styled_df, hide_index=True, use_container_width=True)
    else:
        st.info("최근 이벤트가 없습니다.")

except Exception as e:
    st.error(f"데이터를 불러오는 중 오류가 발생했습니다: {str(e)}")
    st.info("서버 연결을 확인하고 페이지를 새로고침 해주세요.")

# 푸터
st.markdown("---")
st.markdown("© 2023 CryptoLytica - 고성능 암호화폐 데이터 수집 및 분석 플랫폼") 