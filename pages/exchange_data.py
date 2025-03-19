import streamlit as st
import pandas as pd
import sys
import os
from datetime import datetime, timedelta

# 상위 디렉토리 추가하여 api 모듈을 import할 수 있도록 함
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from api.client import CryptoLyticaClient
from utils.visualization import create_candlestick_chart, create_bar_chart
from utils.helpers import format_number, format_currency

# 페이지 설정
st.set_page_config(
    page_title="CryptoLytica - 거래소 데이터",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 사이드바 제목
st.sidebar.title("거래소 데이터")

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

# 거래소 목록 가져오기
@st.cache_data(ttl=300)
def get_exchanges():
    return client.get_exchanges()

# 시장 데이터 가져오기
@st.cache_data(ttl=60)
def get_market_data(exchange, symbol, period="1d", limit=100):
    return client.get_market_data(exchange, symbol, period, limit)

# 페이지 타이틀
st.title("거래소 데이터 분석")

# 거래소 선택
exchanges = get_exchanges()
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

# 데이터 가져오기
st.subheader(f"{currency_pairs[selected_pair]} 데이터 ({selected_exchange_name})")

# 새로고침 버튼
if st.button("데이터 새로고침"):
    st.cache_data.clear()
    st.experimental_rerun()

try:
    # 데이터 로드 중 표시
    with st.spinner(f"{selected_exchange_name}에서 {selected_pair} 데이터를 가져오는 중..."):
        market_data = get_market_data(selected_exchange_id, selected_pair, selected_period, data_limit)
    
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
                    label="24시간 고가",
                    value=format_currency(df["high"].max(), "USDT")
                )
            
            with col3:
                st.metric(
                    label="24시간 저가",
                    value=format_currency(df["low"].min(), "USDT")
                )
            
            with col4:
                st.metric(
                    label="24시간 거래량",
                    value=format_number(df["volume"].sum(), decimal_places=2)
                )
        
        # 차트 표시
        tab1, tab2 = st.tabs(["가격 차트", "거래량 차트"])
        
        with tab1:
            st.plotly_chart(
                create_candlestick_chart(
                    df,
                    title=f"{selected_pair} 가격 차트 ({selected_exchange_name}, {period_options[selected_period]})"
                ),
                use_container_width=True
            )
        
        with tab2:
            # 거래량 차트
            volume_df = df[['timestamp', 'volume']].copy()
            
            st.plotly_chart(
                create_bar_chart(
                    volume_df,
                    'timestamp',
                    'volume',
                    title=f"{selected_pair} 거래량 ({selected_exchange_name}, {period_options[selected_period]})",
                    color='rgba(0, 128, 0, 0.7)'
                ),
                use_container_width=True
            )
        
        # 데이터 테이블
        st.subheader("원시 데이터")
        
        # 데이터 가공
        display_df = df.copy()
        display_df['timestamp'] = display_df['timestamp'].dt.strftime('%Y-%m-%d %H:%M:%S')
        
        for col in ['open', 'high', 'low', 'close']:
            display_df[col] = display_df[col].apply(lambda x: format_currency(x, "USDT"))
        
        display_df['volume'] = display_df['volume'].apply(lambda x: format_number(x, decimal_places=2))
        
        # 표시할 열 이름 변경
        display_df.columns = ["시간", "시가", "고가", "저가", "종가", "거래량"]
        
        st.dataframe(
            display_df,
            hide_index=True,
            use_container_width=True
        )
        
        # CSV 다운로드 버튼
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="CSV로 다운로드",
            data=csv,
            file_name=f"{selected_exchange_id}_{selected_pair}_{selected_period}_{datetime.now().strftime('%Y%m%d')}.csv",
            mime="text/csv"
        )
    else:
        st.warning(f"{selected_pair} 데이터를 가져올 수 없습니다.")

except Exception as e:
    st.error(f"데이터를 불러오는 중 오류가 발생했습니다: {str(e)}")
    st.info("서버 연결을 확인하고 페이지를 새로고침 해주세요.")

# 거래소 정보 표시
st.sidebar.markdown("---")
st.sidebar.subheader("거래소 정보")

try:
    exchange_info = next((ex for ex in exchanges if ex["id"] == selected_exchange_id), None)
    
    if exchange_info:
        st.sidebar.markdown(f"**이름:** {exchange_info['name']}")
        st.sidebar.markdown(f"**상태:** {exchange_info['status']}")
        st.sidebar.markdown(f"**마지막 업데이트:** {exchange_info['last_update']}")
    else:
        st.sidebar.warning("거래소 정보를 찾을 수 없습니다.")
except Exception as e:
    st.sidebar.error(f"거래소 정보를 불러오는 중 오류가 발생했습니다: {str(e)}")

# 푸터
st.markdown("---")
st.markdown("© 2023 CryptoLytica - 고성능 암호화폐 데이터 수집 및 분석 플랫폼") 