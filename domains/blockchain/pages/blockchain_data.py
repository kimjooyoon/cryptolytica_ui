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

from domains.blockchain.services.blockchain_client import BlockchainClient
from domains.blockchain.utils.blockchain_utils import categorize_blockchain_activity, wallet_risk_score
from shared.utils.visualization import create_line_chart, create_bar_chart, create_scatter_plot, create_heatmap
from shared.utils.helpers import format_number, format_currency, time_ago, shorten_address
from core.config import get_config_value
from core.state import get_domain_state, set_domain_state

# 페이지 타이틀
page_title = "블록체인 데이터"

def render_page():
    """블록체인 데이터 페이지를 렌더링합니다."""
    
    # 사이드바 제목
    st.sidebar.title("블록체인 데이터")
    
    # API 클라이언트 생성
    client = get_blockchain_client()
    
    # 블록체인 목록 가져오기
    blockchains = get_blockchains(client)
    
    # 블록체인 선택
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
    
    # 상태 저장
    set_domain_state('blockchain', 'selected_blockchain_id', selected_blockchain_id)
    set_domain_state('blockchain', 'data_type', data_type)
    set_domain_state('blockchain', 'period', selected_period)
    set_domain_state('blockchain', 'limit', data_limit)
    
    # 페이지 타이틀
    st.title("블록체인 데이터 분석")
    
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
                render_transaction_stats(client, selected_blockchain_id, selected_blockchain_name, data_limit)
            elif data_type == "주요 지갑 활동":
                render_wallet_activities(client, selected_blockchain_id, selected_blockchain_name, data_limit)
            elif data_type == "스마트 컨트랙트 활동":
                render_contract_activities(client, selected_blockchain_id, selected_blockchain_name, data_limit)
        
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

def render_transaction_stats(client, blockchain_id, blockchain_name, limit):
    """트랜잭션 통계를 렌더링합니다."""
    st.subheader(f"{blockchain_name} 트랜잭션 통계")
    
    # 트랜잭션 데이터 가져오기
    transactions = client.get_blockchain_transactions(blockchain_id, limit)
    transactions_df = pd.DataFrame([{
        "timestamp": tx.timestamp,
        "tx_count": tx.tx_count,
        "avg_fee": tx.avg_fee,
        "block_size": tx.block_size,
        "active_addresses": tx.active_addresses,
        "network_hashrate": tx.network_hashrate
    } for tx in transactions])
    
    # 트랜잭션 차트
    # 탭 생성
    tabs = st.tabs(["트랜잭션 수", "평균 수수료", "블록 크기", "활성 주소"])
    
    with tabs[0]:
        st.plotly_chart(
            create_line_chart(
                transactions_df,
                'timestamp',
                ['tx_count'],
                title=f"{blockchain_name} 트랜잭션 수"
            ),
            use_container_width=True
        )
    
    with tabs[1]:
        st.plotly_chart(
            create_line_chart(
                transactions_df,
                'timestamp',
                ['avg_fee'],
                title=f"{blockchain_name} 평균 수수료"
            ),
            use_container_width=True
        )
    
    with tabs[2]:
        st.plotly_chart(
            create_line_chart(
                transactions_df,
                'timestamp',
                ['block_size'],
                title=f"{blockchain_name} 블록 크기 (MB)"
            ),
            use_container_width=True
        )
    
    with tabs[3]:
        st.plotly_chart(
            create_line_chart(
                transactions_df,
                'timestamp',
                ['active_addresses'],
                title=f"{blockchain_name} 활성 주소 수"
            ),
            use_container_width=True
        )
    
    # 네트워크 해시레이트 (비트코인의 경우)
    if blockchain_id == "bitcoin" and 'network_hashrate' in transactions_df.columns:
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
        file_name=f"{blockchain_id}_transactions_{datetime.now().strftime('%Y%m%d')}.csv",
        mime="text/csv"
    )

def render_wallet_activities(client, blockchain_id, blockchain_name, limit):
    """지갑 활동 정보를 렌더링합니다."""
    st.subheader(f"{blockchain_name} 주요 지갑 활동")
    
    # 지갑 활동 데이터 가져오기
    wallet_activities = client.get_wallet_activities(blockchain_id, limit)
    wallet_activities_df = pd.DataFrame([{
        "address": wa.address,
        "timestamp": wa.timestamp,
        "amount": wa.amount,
        "direction": wa.direction,
        "transaction_hash": wa.transaction_hash,
        "activity_type": wa.activity_type
    } for wa in wallet_activities])
    
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
    display_df['address'] = display_df['address'].apply(shorten_address)
    display_df['transaction_hash'] = display_df['transaction_hash'].apply(shorten_address)
    
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

def render_contract_activities(client, blockchain_id, blockchain_name, limit):
    """스마트 컨트랙트 활동 정보를 렌더링합니다."""
    # 이더리움, 솔라나 등의 스마트 컨트랙트 활동 데이터
    if blockchain_id in ["ethereum", "solana", "cardano"]:
        st.subheader(f"{blockchain_name} 스마트 컨트랙트 활동")
        
        # 스마트 컨트랙트 데이터 가져오기
        contract_activities = client.get_contract_activities(blockchain_id, limit)
        
        if contract_activities:
            contract_activities_df = pd.DataFrame([{
                "timestamp": ca.timestamp,
                "contract_address": ca.contract_address,
                "activity_type": ca.activity_type,
                "volume": ca.volume,
                "transaction_count": ca.transaction_count,
                "unique_users": ca.unique_users
            } for ca in contract_activities])
            
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
                        title=f"{blockchain_name} 활동 유형별 볼륨"
                    ),
                    use_container_width=True
                )
            
            with tabs[1]:
                st.plotly_chart(
                    create_bar_chart(
                        activity_stats,
                        'activity_type',
                        'transaction_count',
                        title=f"{blockchain_name} 활동 유형별 트랜잭션 수"
                    ),
                    use_container_width=True
                )
            
            with tabs[2]:
                st.plotly_chart(
                    create_bar_chart(
                        activity_stats,
                        'activity_type',
                        'unique_users',
                        title=f"{blockchain_name} 활동 유형별 고유 사용자 수"
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
                    title=f"{blockchain_name} 시간별 스마트 컨트랙트 볼륨"
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
            top_contracts['contract_address'] = top_contracts['contract_address'].apply(shorten_address)
            
            # 컬럼명 변경
            top_contracts.columns = ["컨트랙트 주소", "볼륨", "트랜잭션 수", "고유 사용자 수"]
            
            st.dataframe(
                top_contracts,
                hide_index=True,
                use_container_width=True
            )
        else:
            st.info(f"{blockchain_name}에 대한 스마트 컨트랙트 데이터가 없습니다.")
    else:
        st.info(f"{blockchain_name}은(는) 스마트 컨트랙트를 지원하지 않거나 데이터가 없습니다.")

@st.cache_resource
def get_blockchain_client():
    """블록체인 API 클라이언트를 생성합니다."""
    api_base_url = get_config_value("api.base_url", "http://localhost:8000")
    api_key = get_config_value("api.api_key", "")
    ws_url = get_config_value("api.ws_url", "")
    
    return BlockchainClient(api_base_url, api_key, ws_url)

@st.cache_data(ttl=300)
def get_blockchains(client):
    """블록체인 목록을 가져옵니다."""
    return client.get_blockchains()