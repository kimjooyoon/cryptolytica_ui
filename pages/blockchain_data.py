import streamlit as st
import pandas as pd
import sys
import os
from datetime import datetime, timedelta
import random

# 상위 디렉토리 추가하여 api 모듈을 import할 수 있도록 함
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from api.client import CryptoLyticaClient
from utils.visualization import create_line_chart, create_bar_chart, create_scatter_plot, create_heatmap
from utils.helpers import format_number, format_currency, time_ago

# 페이지 설정
st.set_page_config(
    page_title="CryptoLytica - 블록체인 데이터",
    page_icon="⛓️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 사이드바 제목
st.sidebar.title("블록체인 데이터")

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

# 블록체인 목록 가져오기
@st.cache_data(ttl=300)
def get_blockchains():
    return client.get_blockchains()

# 가상의 블록체인 트랜잭션 데이터 생성
@st.cache_data(ttl=60)
def get_blockchain_transactions(blockchain, limit=100):
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

# 가상의 지갑 활동 데이터 생성
@st.cache_data(ttl=300)
def get_wallet_activities(blockchain, limit=10):
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

# 가상의 스마트 컨트랙트 활동 생성 (이더리움, 솔라나 등)
@st.cache_data(ttl=120)
def get_contract_activities(blockchain, limit=100):
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

# 페이지 타이틀
st.title("블록체인 데이터 분석")

# 블록체인 선택
blockchains = get_blockchains()
blockchain_names = [blockchain["name"] for blockchain in blockchains]
blockchain_ids = [blockchain["id"] for blockchain in blockchains]

selected_blockchain_name = st.sidebar.selectbox(
    "블록체인 선택",
    options=blockchain_names,
    index=0
)

selected_blockchain_id = blockchain_ids[blockchain_names.index(selected_blockchain_name)]

# 데이터 타입 선택
data_type = st.sidebar.radio(
    "데이터 유형",
    options=["트랜잭션 통계", "주요 지갑 활동", "스마트 컨트랙트 활동"]
)

# 기간 선택
period_options = {
    "1h": "1시간",
    "24h": "24시간",
    "7d": "7일",
    "30d": "30일"
}

selected_period = st.sidebar.selectbox(
    "기간 선택",
    options=list(period_options.keys()),
    index=1,
    format_func=lambda x: period_options[x]
)

# 데이터 한도 설정
if data_type == "주요 지갑 활동":
    data_limit = st.sidebar.slider(
        "표시할 지갑 수",
        min_value=5,
        max_value=50,
        value=10,
        step=5
    )
else:
    data_limit = st.sidebar.slider(
        "데이터 수량",
        min_value=10,
        max_value=200,
        value=100,
        step=10
    )

# 새로고침 버튼
if st.button("데이터 새로고침"):
    st.cache_data.clear()
    st.experimental_rerun()

# 블록체인 정보 표시
try:
    blockchain_info = next((b for b in blockchains if b["id"] == selected_blockchain_id), None)
    
    if blockchain_info:
        # 블록체인 상태 정보
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric(
                label="네트워크 상태",
                value=blockchain_info["status"],
                delta="정상" if blockchain_info["status"] == "synced" else "동기화 중"
            )
        
        with col2:
            st.metric(
                label="최신 블록",
                value=format_number(blockchain_info["last_block"], decimal_places=0)
            )
        
        with col3:
            last_update_time = datetime.fromisoformat(blockchain_info["last_update"].replace('Z', '+00:00'))
            st.metric(
                label="마지막 업데이트",
                value=time_ago(last_update_time)
            )
        
        # 선택된 데이터 타입에 따라 다른 내용 표시
        if data_type == "트랜잭션 통계":
            st.subheader(f"{selected_blockchain_name} 트랜잭션 통계")
            
            # 트랜잭션 데이터 가져오기
            transactions_df = get_blockchain_transactions(selected_blockchain_id, data_limit)
            
            # 트랜잭션 차트
            # 탭 생성
            tabs = st.tabs(["트랜잭션 수", "평균 수수료", "블록 크기", "활성 주소"])
            
            with tabs[0]:
                st.plotly_chart(
                    create_line_chart(
                        transactions_df,
                        'timestamp',
                        ['tx_count'],
                        title=f"{selected_blockchain_name} 트랜잭션 수"
                    ),
                    use_container_width=True
                )
            
            with tabs[1]:
                st.plotly_chart(
                    create_line_chart(
                        transactions_df,
                        'timestamp',
                        ['avg_fee'],
                        title=f"{selected_blockchain_name} 평균 수수료"
                    ),
                    use_container_width=True
                )
            
            with tabs[2]:
                st.plotly_chart(
                    create_line_chart(
                        transactions_df,
                        'timestamp',
                        ['block_size'],
                        title=f"{selected_blockchain_name} 블록 크기 (MB)"
                    ),
                    use_container_width=True
                )
            
            with tabs[3]:
                st.plotly_chart(
                    create_line_chart(
                        transactions_df,
                        'timestamp',
                        ['active_addresses'],
                        title=f"{selected_blockchain_name} 활성 주소 수"
                    ),
                    use_container_width=True
                )
            
            # 네트워크 해시레이트 (비트코인의 경우)
            if selected_blockchain_id == "bitcoin" and 'network_hashrate' in transactions_df.columns:
                st.subheader("네트워크 해시레이트")
                st.plotly_chart(
                    create_line_chart(
                        transactions_df,
                        'timestamp',
                        ['network_hashrate'],
                        title="비트코인 네트워크 해시레이트 (EH/s)"
                    ),
                    use_container_width=True
                )
            
            # 트랜잭션 데이터 테이블
            st.subheader("원시 데이터")
            
            # 데이터 가공
            display_df = transactions_df.copy()
            display_df['timestamp'] = display_df['timestamp'].dt.strftime('%Y-%m-%d %H:%M:%S')
            
            if 'network_hashrate' in display_df.columns:
                cols_to_display = ['timestamp', 'tx_count', 'avg_fee', 'block_size', 'active_addresses', 'network_hashrate']
                col_names = ["시간", "트랜잭션 수", "평균 수수료", "블록 크기 (MB)", "활성 주소 수", "해시레이트 (EH/s)"]
            else:
                cols_to_display = ['timestamp', 'tx_count', 'avg_fee', 'block_size', 'active_addresses']
                col_names = ["시간", "트랜잭션 수", "평균 수수료", "블록 크기 (MB)", "활성 주소 수"]
            
            display_df = display_df[cols_to_display]
            display_df.columns = col_names
            
            st.dataframe(
                display_df,
                hide_index=True,
                use_container_width=True
            )
            
            # CSV 다운로드 버튼
            csv = transactions_df.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="CSV로 다운로드",
                data=csv,
                file_name=f"{selected_blockchain_id}_transactions_{datetime.now().strftime('%Y%m%d')}.csv",
                mime="text/csv"
            )
        
        elif data_type == "주요 지갑 활동":
            st.subheader(f"{selected_blockchain_name} 주요 지갑 활동")
            
            # 지갑 활동 데이터 가져오기
            wallet_activities_df = get_wallet_activities(selected_blockchain_id, data_limit)
            
            # 지갑 활동 시각화
            col1, col2 = st.columns(2)
            
            with col1:
                # 방향별 활동 분포
                direction_counts = wallet_activities_df['direction'].value_counts()
                st.plotly_chart(
                    create_bar_chart(
                        pd.DataFrame({'direction': direction_counts.index, 'count': direction_counts.values}),
                        'direction',
                        'count',
                        title="입/출금 활동 분포",
                        color='rgba(55, 83, 109, 0.7)'
                    ),
                    use_container_width=True
                )
            
            with col2:
                # 활동 유형별 분포
                activity_counts = wallet_activities_df['activity_type'].value_counts()
                st.plotly_chart(
                    create_bar_chart(
                        pd.DataFrame({'activity_type': activity_counts.index, 'count': activity_counts.values}),
                        'activity_type',
                        'count',
                        title="활동 유형 분포",
                        color='rgba(0, 128, 0, 0.7)'
                    ),
                    use_container_width=True
                )
            
            # 지갑 활동 테이블
            st.subheader("최근 지갑 활동")
            
            # 데이터 정렬 및 가공
            display_df = wallet_activities_df.sort_values('timestamp', ascending=False).copy()
            display_df['timestamp'] = display_df['timestamp'].dt.strftime('%Y-%m-%d %H:%M:%S')
            display_df['amount'] = display_df['amount'].apply(lambda x: format_number(x, decimal_places=6))
            
            # 읽기 쉬운 주소 형식으로 변환 (앞부분과 뒷부분만 표시)
            display_df['address'] = display_df['address'].apply(lambda x: f"{x[:6]}...{x[-4:]}")
            display_df['transaction_hash'] = display_df['transaction_hash'].apply(lambda x: f"{x[:6]}...{x[-4:]}")
            
            # 컬럼명 변경
            display_df.columns = ["주소", "시간", "금액", "방향", "트랜잭션 해시", "활동 유형"]
            
            # 방향에 따라 색상 적용
            def highlight_direction(val):
                if val == "in":
                    return 'background-color: #c6efce; color: #006100'
                elif val == "out":
                    return 'background-color: #ffc7ce; color: #9c0006'
                return ''
            
            # 스타일 적용된 데이터프레임 표시
            styled_df = display_df.style.applymap(
                highlight_direction, subset=['방향']
            )
            
            st.dataframe(
                styled_df,
                hide_index=True,
                use_container_width=True
            )
            
            # 특정 지갑 주소 검색 기능
            st.subheader("지갑 주소 검색")
            wallet_address = st.text_input("검색할 지갑 주소 입력")
            
            if wallet_address:
                st.info(f"지갑 주소 '{wallet_address}'에 대한 데이터가 준비되면 여기에 표시됩니다.")
        
        elif data_type == "스마트 컨트랙트 활동":
            # 이더리움, 솔라나 등의 스마트 컨트랙트 활동 데이터
            if selected_blockchain_id in ["ethereum", "solana", "cardano"]:
                st.subheader(f"{selected_blockchain_name} 스마트 컨트랙트 활동")
                
                # 스마트 컨트랙트 데이터 가져오기
                contract_activities_df = get_contract_activities(selected_blockchain_id, data_limit)
                
                if not contract_activities_df.empty:
                    # 활동 유형별 통계
                    activity_stats = contract_activities_df.groupby('activity_type').agg({
                        'volume': 'sum',
                        'transaction_count': 'sum',
                        'unique_users': 'sum'
                    }).reset_index()
                    
                    # 탭 생성
                    tabs = st.tabs(["활동 볼륨", "트랜잭션 수", "고유 사용자 수"])
                    
                    with tabs[0]:
                        st.plotly_chart(
                            create_bar_chart(
                                activity_stats,
                                'activity_type',
                                'volume',
                                title=f"{selected_blockchain_name} 활동 유형별 볼륨"
                            ),
                            use_container_width=True
                        )
                    
                    with tabs[1]:
                        st.plotly_chart(
                            create_bar_chart(
                                activity_stats,
                                'activity_type',
                                'transaction_count',
                                title=f"{selected_blockchain_name} 활동 유형별 트랜잭션 수"
                            ),
                            use_container_width=True
                        )
                    
                    with tabs[2]:
                        st.plotly_chart(
                            create_bar_chart(
                                activity_stats,
                                'activity_type',
                                'unique_users',
                                title=f"{selected_blockchain_name} 활동 유형별 고유 사용자 수"
                            ),
                            use_container_width=True
                        )
                    
                    # 시간별 활동 추이
                    st.subheader("시간별 활동 추이")
                    
                    time_series = contract_activities_df.copy()
                    time_series['timestamp'] = pd.to_datetime(time_series['timestamp'])
                    time_series = time_series.set_index('timestamp')
                    time_series = time_series.resample('1H').agg({
                        'volume': 'sum',
                        'transaction_count': 'sum',
                        'unique_users': 'mean'
                    }).reset_index()
                    
                    st.plotly_chart(
                        create_line_chart(
                            time_series,
                            'timestamp',
                            ['volume'],
                            title=f"{selected_blockchain_name} 시간별 스마트 컨트랙트 볼륨"
                        ),
                        use_container_width=True
                    )
                    
                    # 상위 스마트 컨트랙트
                    st.subheader("상위 스마트 컨트랙트")
                    
                    top_contracts = contract_activities_df.groupby('contract_address').agg({
                        'volume': 'sum',
                        'transaction_count': 'sum',
                        'unique_users': 'sum'
                    }).reset_index().sort_values('volume', ascending=False).head(10)
                    
                    # 읽기 쉬운 주소 형식으로 변환
                    top_contracts['contract_address'] = top_contracts['contract_address'].apply(lambda x: f"{x[:6]}...{x[-4:]}")
                    
                    # 컬럼명 변경
                    top_contracts.columns = ["컨트랙트 주소", "볼륨", "트랜잭션 수", "고유 사용자 수"]
                    
                    st.dataframe(
                        top_contracts,
                        hide_index=True,
                        use_container_width=True
                    )
                else:
                    st.info(f"{selected_blockchain_name}에 대한 스마트 컨트랙트 데이터가 없습니다.")
            else:
                st.info(f"{selected_blockchain_name}은(는) 스마트 컨트랙트를 지원하지 않거나 데이터가 없습니다.")
    
    else:
        st.warning(f"선택한 블록체인 '{selected_blockchain_name}'에 대한 정보를 찾을 수 없습니다.")

except Exception as e:
    st.error(f"데이터를 불러오는 중 오류가 발생했습니다: {str(e)}")
    st.info("서버 연결을 확인하고 페이지를 새로고침 해주세요.")

# 블록체인 정보 표시
st.sidebar.markdown("---")
st.sidebar.subheader("블록체인 정보")

try:
    blockchain_info = next((b for b in blockchains if b["id"] == selected_blockchain_id), None)
    
    if blockchain_info:
        st.sidebar.markdown(f"**이름:** {blockchain_info['name']}")
        st.sidebar.markdown(f"**상태:** {blockchain_info['status']}")
        st.sidebar.markdown(f"**최신 블록:** {blockchain_info['last_block']}")
        st.sidebar.markdown(f"**마지막 업데이트:** {blockchain_info['last_update']}")
    else:
        st.sidebar.warning("블록체인 정보를 찾을 수 없습니다.")
except Exception as e:
    st.sidebar.error(f"블록체인 정보를 불러오는 중 오류가 발생했습니다: {str(e)}")

# 푸터
st.markdown("---")
st.markdown("© 2023 CryptoLytica - 고성능 암호화폐 데이터 수집 및 분석 플랫폼") 