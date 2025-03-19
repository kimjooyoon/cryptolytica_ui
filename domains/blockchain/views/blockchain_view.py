"""
블록체인 데이터 관련 Streamlit 뷰 컴포넌트
"""
import streamlit as st
import pandas as pd
from datetime import datetime
from typing import Dict, Any, List, Optional

from utils.visualization import create_line_chart, create_bar_chart, create_scatter_plot, create_heatmap
from utils.helpers import format_number, format_currency, time_ago
from domains.blockchain.services.blockchain_service import BlockchainService
from domains.blockchain.utils.blockchain_utils import (
    format_blockchain_status,
    format_transaction_hash,
    format_address,
    categorize_transaction_volume
)


def render_blockchain_view():
    """블록체인 데이터 페이지 렌더링"""
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
        from api.client import CryptoLyticaClient
        api_config = config.get('api', {})
        return CryptoLyticaClient(
            base_url=api_config.get('base_url', 'http://localhost:8000'),
            api_key=api_config.get('api_key', ''),
            ws_url=api_config.get('ws_url', '')
        )

    client = get_api_client()
    blockchain_service = BlockchainService(client)

    # 페이지 타이틀
    st.title("블록체인 데이터 분석")

    # 블록체인 목록 가져오기
    blockchains = blockchain_service.get_blockchains()
    blockchain_names = [blockchain["name"] for blockchain in blockchains]
    blockchain_ids = [blockchain["id"] for blockchain in blockchains]

    # 블록체인 선택
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
    render_blockchain_info(blockchain_service, selected_blockchain_id)
    
    # 선택된 데이터 타입에 따라 다른 내용 표시
    if data_type == "트랜잭션 통계":
        render_transaction_stats(blockchain_service, selected_blockchain_id, selected_blockchain_name, data_limit)
    elif data_type == "주요 지갑 활동":
        render_wallet_activities(blockchain_service, selected_blockchain_id, selected_blockchain_name, data_limit)
    elif data_type == "스마트 컨트랙트 활동":
        render_contract_activities(blockchain_service, selected_blockchain_id, selected_blockchain_name, data_limit)


def render_blockchain_info(blockchain_service: BlockchainService, blockchain_id: str):
    """블록체인 기본 정보 렌더링"""
    try:
        blockchain_info = blockchain_service.get_blockchain_by_id(blockchain_id)
        
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
    except Exception as e:
        st.error(f"블록체인 정보를 불러오는 중 오류가 발생했습니다: {str(e)}")


def render_transaction_stats(blockchain_service: BlockchainService, blockchain_id: str, blockchain_name: str, limit: int):
    """트랜잭션 통계 렌더링"""
    st.subheader(f"{blockchain_name} 트랜잭션 통계")
    
    # 트랜잭션 데이터 가져오기
    transactions_df = blockchain_service.get_blockchain_transactions(blockchain_id, limit)
    
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
    
    # 트랜잭션 데이터 테이블
    st.subheader("트랜잭션 데이터")
    st.dataframe(transactions_df)


def render_wallet_activities(blockchain_service: BlockchainService, blockchain_id: str, blockchain_name: str, limit: int):
    """지갑 활동 렌더링"""
    st.subheader(f"{blockchain_name} 주요 지갑 활동")
    
    wallet_activities = blockchain_service.get_wallet_activities(blockchain_id, limit)
    
    # 지갑 활동 표시
    if not wallet_activities.empty:
        # 방향별 활동 차트
        direction_counts = wallet_activities['direction'].value_counts()
        st.plotly_chart(
            create_pie_chart(
                direction_counts,
                title="거래 방향 분포"
            ),
            use_container_width=True
        )
        
        # 활동 유형별 차트
        activity_counts = wallet_activities['activity_type'].value_counts()
        st.plotly_chart(
            create_bar_chart(
                pd.DataFrame({'활동 유형': activity_counts.index, '횟수': activity_counts.values}),
                x='활동 유형',
                y='횟수',
                title="활동 유형별 횟수"
            ),
            use_container_width=True
        )
        
        # 지갑 활동 목록
        st.subheader("최근 지갑 활동")
        st.dataframe(wallet_activities)
    else:
        st.info(f"{blockchain_name}에 대한 지갑 활동 데이터가 없습니다.")


def render_contract_activities(blockchain_service: BlockchainService, blockchain_id: str, blockchain_name: str, limit: int):
    """스마트 컨트랙트 활동 렌더링"""
    st.subheader(f"{blockchain_name} 스마트 컨트랙트 활동")
    
    contract_activities = blockchain_service.get_contract_activities(blockchain_id, limit)
    
    if not contract_activities.empty:
        # 활동 유형별 분포
        activity_counts = contract_activities['activity_type'].value_counts()
        st.plotly_chart(
            create_pie_chart(
                activity_counts,
                title="컨트랙트 활동 유형 분포"
            ),
            use_container_width=True
        )
        
        # 컨트랙트 활동 시계열
        st.plotly_chart(
            create_line_chart(
                contract_activities,
                'timestamp',
                ['volume'],
                title=f"{blockchain_name} 컨트랙트 볼륨 추이"
            ),
            use_container_width=True
        )
        
        # 거래 및 사용자 상관관계
        st.plotly_chart(
            create_scatter_plot(
                contract_activities,
                x='transaction_count',
                y='unique_users',
                size='volume',
                color='activity_type',
                title="트랜잭션 수 vs 고유 사용자 수"
            ),
            use_container_width=True
        )
        
        # 컨트랙트 활동 데이터 표시
        st.subheader("컨트랙트 활동 데이터")
        st.dataframe(contract_activities)
    else:
        st.info(f"{blockchain_name}에 대한 스마트 컨트랙트 활동 데이터가 없습니다.")


def create_pie_chart(series, title=""):
    """파이 차트 생성 (Plotly)"""
    import plotly.express as px
    
    fig = px.pie(
        values=series.values, 
        names=series.index, 
        title=title,
        color_discrete_sequence=px.colors.qualitative.Pastel
    )
    fig.update_traces(textposition='inside', textinfo='percent+label')
    fig.update_layout(uniformtext_minsize=12, uniformtext_mode='hide')
    
    return fig 