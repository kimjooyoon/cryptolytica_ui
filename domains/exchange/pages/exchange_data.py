import streamlit as st
import pandas as pd
import sys
import os
from datetime import datetime, timedelta
from pathlib import Path

# 상위 디렉토리 경로 추가
ROOT_DIR = Path(__file__).parent.parent.parent.parent
sys.path.append(str(ROOT_DIR))

from domains.exchange.services.exchange_client import ExchangeClient
from shared.utils.visualization import create_candlestick_chart, create_bar_chart
from shared.utils.helpers import format_number, format_currency, format_percentage
from core.config import get_config_value
from core.state import get_domain_state, set_domain_state

# 페이지 타이틀
page_title = "거래소 데이터"

def render_page():
    """거래소 데이터 페이지를 렌더링합니다."""
    
    # 사이드바 제목
    st.sidebar.title("거래소 데이터")
    
    # API 클라이언트 생성
    client = get_exchange_client()
    
    # 거래소 목록 가져오기
    exchanges = get_exchanges(client)
    
    # 페이지 타이틀
    st.title("거래소 데이터 분석")
    
    # 거래소 선택
    exchange_names = [exchange["name"] for exchange in exchanges]
    exchange_ids = [exchange["id"] for exchange in exchanges]
    
    selected_exchange_name = st.sidebar.selectbox(
        "거래소 선택",
        options=exchange_names,
        index=0
    )
    
    selected_exchange_id = exchange_ids[exchange_names.index(selected_exchange_name)]
    
    # 통화쌍 선택 (가상 데이터)
    currency_pairs = {
        "BTC/USDT": "Bitcoin/USDT",
        "ETH/USDT": "Ethereum/USDT",
        "SOL/USDT": "Solana/USDT",
        "ADA/USDT": "Cardano/USDT",
        "XRP/USDT": "Ripple/USDT",
        "DOGE/USDT": "Dogecoin/USDT",
        "DOT/USDT": "Polkadot/USDT",
        "AVAX/USDT": "Avalanche/USDT"
    }
    
    selected_pair = st.sidebar.selectbox(
        "통화쌍 선택",
        options=list(currency_pairs.keys()),
        index=0,
        format_func=lambda x: currency_pairs[x]
    )
    
    # 기간 선택
    period_options = {
        "1h": "1시간",
        "4h": "4시간",
        "1d": "1일",
        "1w": "1주일",
        "1M": "1개월"
    }
    
    selected_period = st.sidebar.selectbox(
        "기간 선택",
        options=list(period_options.keys()),
        index=2,
        format_func=lambda x: period_options[x]
    )
    
    # 데이터 한도 선택
    data_limit = st.sidebar.slider(
        "데이터 수량",
        min_value=20,
        max_value=200,
        value=100,
        step=10
    )
    
    # 상태 저장
    set_domain_state('exchange', 'selected_exchange_id', selected_exchange_id)
    set_domain_state('exchange', 'selected_pair', selected_pair)
    set_domain_state('exchange', 'period', selected_period)
    set_domain_state('exchange', 'limit', data_limit)
    
    # 데이터 가져오기
    st.subheader(f"{currency_pairs[selected_pair]} 데이터 ({selected_exchange_name})")
    
    # 새로고침 버튼
    if st.button("데이터 새로고침"):
        st.cache_data.clear()
        st.experimental_rerun()
    
    try:
        # 데이터 로드 중 표시
        with st.spinner(f"{selected_exchange_name}에서 {selected_pair} 데이터를 가져오는 중..."):
            market_data = get_market_data(client, selected_exchange_id, selected_pair, selected_period, data_limit)
        
        if market_data and "data" in market_data:
            # 데이터프레임으로 변환
            df = pd.DataFrame(market_data["data"])
            
            # 타임스탬프를 datetime으로 변환
            df['timestamp'] = pd.to_datetime(df['timestamp'])
            
            # 최신 데이터 표시
            latest_data = df.iloc[-1] if not df.empty else None
            
            if latest_data is not None:
                # 최신 가격 정보
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    st.metric(
                        label="최신 가격",
                        value=format_currency(latest_data["close"], "USDT"),
                        delta=format_percentage((latest_data["close"] - df.iloc[-2]["close"]) / df.iloc[-2]["close"]) if len(df) > 1 else None
                    )
                
                with col2:
                    st.metric(
                        label="24시간 거래량",
                        value=format_number(latest_data["volume"], decimal_places=2),
                        delta=format_percentage((latest_data["volume"] - df.iloc[-2]["volume"]) / df.iloc[-2]["volume"]) if len(df) > 1 else None
                    )
                
                with col3:
                    st.metric(
                        label="최고가",
                        value=format_currency(latest_data["high"], "USDT")
                    )
                
                with col4:
                    st.metric(
                        label="최저가",
                        value=format_currency(latest_data["low"], "USDT")
                    )
                
                # 캔들스틱 차트 생성
                fig = create_candlestick_chart(
                    df,
                    timestamp_col='timestamp',
                    open_col='open',
                    high_col='high',
                    low_col='low',
                    close_col='close',
                    volume_col='volume',
                    title=f"{selected_pair} 가격 차트 ({selected_period})"
                )
                
                st.plotly_chart(fig, use_container_width=True)
                
                # 거래량 차트 생성
                volume_fig = create_bar_chart(
                    df,
                    x_col='timestamp',
                    y_col='volume',
                    title=f"{selected_pair} 거래량 차트 ({selected_period})"
                )
                
                st.plotly_chart(volume_fig, use_container_width=True)
                
                # 거래 데이터 표 (최근 10개)
                st.subheader("최근 거래 데이터")
                
                df_display = df.tail(10).copy()
                df_display["시간"] = df_display["timestamp"].dt.strftime("%Y-%m-%d %H:%M")
                df_display["시가"] = df_display["open"].apply(lambda x: format_currency(x, "USDT"))
                df_display["고가"] = df_display["high"].apply(lambda x: format_currency(x, "USDT"))
                df_display["저가"] = df_display["low"].apply(lambda x: format_currency(x, "USDT"))
                df_display["종가"] = df_display["close"].apply(lambda x: format_currency(x, "USDT"))
                df_display["거래량"] = df_display["volume"].apply(lambda x: format_number(x, decimal_places=2))
                
                st.dataframe(
                    df_display[["시간", "시가", "고가", "저가", "종가", "거래량"]],
                    use_container_width=True,
                    hide_index=True
                )
            else:
                st.warning("표시할 데이터가 없습니다.")
        else:
            st.warning(f"{selected_exchange_name}에서 {selected_pair}에 대한 데이터를 가져올 수 없습니다.")
    
    except Exception as e:
        st.error(f"데이터를 불러오는 중 오류가 발생했습니다: {str(e)}")
        st.info("거래소 연결을 확인하고 페이지를 새로고침 해주세요.")

# API 클라이언트 생성
@st.cache_resource
def get_exchange_client():
    base_url = get_config_value('api.base_url', 'http://localhost:8000')
    api_key = get_config_value('api.api_key', '')
    ws_url = get_config_value('api.ws_url', '')
    return ExchangeClient(base_url=base_url, api_key=api_key, ws_url=ws_url)

# 거래소 목록 가져오기
@st.cache_data(ttl=300)
def get_exchanges(client):
    return client.get_exchanges()

# 시장 데이터 가져오기
@st.cache_data(ttl=60)
def get_market_data(client, exchange, symbol, period="1d", limit=100):
    return client.get_market_data(exchange, symbol, period, limit) 