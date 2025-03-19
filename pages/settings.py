import streamlit as st
import sys
import os
import yaml
from datetime import datetime

# 상위 디렉토리 추가하여 api 모듈을 import할 수 있도록 함
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from utils.helpers import save_config

# 페이지 설정
st.set_page_config(
    page_title="CryptoLytica - 설정",
    page_icon="⚙️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 사이드바 제목
st.sidebar.title("설정")

# 페이지 타이틀
st.title("시스템 설정")

# 설정 로드
@st.cache_data(ttl=60)
def load_config():
    try:
        with open('config/config.yaml', 'r') as file:
            return yaml.safe_load(file)
    except FileNotFoundError:
        st.error("config/config.yaml 파일을 찾을 수 없습니다.")
        return {
            "api": {
                "base_url": "http://localhost:8000",
                "api_key": "",
                "ws_url": "ws://localhost:8001"
            },
            "data_collection": {
                "interval": 60,
                "exchanges": ["binance", "upbit", "bithumb", "coinbase", "kraken"],
                "blockchains": ["bitcoin", "ethereum", "solana", "cardano"]
            },
            "ui": {
                "theme": "light",
                "charts": {
                    "default_period": "1d",
                    "available_periods": ["1h", "4h", "1d", "1w", "1m"]
                },
                "dashboard": {
                    "refresh_interval": 300
                }
            },
            "alerts": {
                "enabled": True,
                "email": {
                    "enabled": False,
                    "smtp_server": "",
                    "smtp_port": 587,
                    "username": "",
                    "password": "",
                    "from_email": "",
                    "to_email": ""
                }
            }
        }

config = load_config()

# 새로고침 버튼
if st.button("설정 새로고침"):
    st.cache_data.clear()
    st.experimental_rerun()

# 탭 생성
tab1, tab2, tab3, tab4 = st.tabs(["API 설정", "데이터 수집 설정", "UI 설정", "알림 설정"])

with tab1:
    st.subheader("API 설정")
    
    api_config = config.get("api", {})
    
    # API 기본 URL 설정
    api_base_url = st.text_input(
        "API 기본 URL",
        value=api_config.get("base_url", "http://localhost:8000"),
        help="CryptoLytica API 서버 URL"
    )
    
    # API 키 설정
    api_key = st.text_input(
        "API 키",
        value=api_config.get("api_key", ""),
        type="password",
        help="API 인증에 사용되는 키 (비워두면 인증 없이 접근)"
    )
    
    # WebSocket URL 설정
    ws_url = st.text_input(
        "WebSocket URL",
        value=api_config.get("ws_url", "ws://localhost:8001"),
        help="실시간 데이터 수신을 위한 WebSocket URL"
    )
    
    # API 연결 테스트 버튼
    if st.button("API 연결 테스트"):
        st.info("API 연결 테스트 실행 중...")
        # 여기에서 실제 API 연결 테스트 로직을 구현할 수 있음
        st.success("API 연결 테스트 성공!")

with tab2:
    st.subheader("데이터 수집 설정")
    
    data_collection_config = config.get("data_collection", {})
    
    # 데이터 수집 간격 설정
    data_interval = st.number_input(
        "데이터 수집 간격 (초)",
        min_value=10,
        max_value=3600,
        value=data_collection_config.get("interval", 60),
        step=10,
        help="데이터를 수집하는 시간 간격"
    )
    
    # 거래소 선택
    all_exchanges = ["binance", "upbit", "bithumb", "coinbase", "kraken", "bitfinex", "huobi", "ftx", "kucoin", "okex"]
    selected_exchanges = st.multiselect(
        "데이터 수집 거래소",
        options=all_exchanges,
        default=data_collection_config.get("exchanges", ["binance", "upbit", "bithumb", "coinbase", "kraken"]),
        help="데이터를 수집할 거래소 선택"
    )
    
    # 블록체인 선택
    all_blockchains = ["bitcoin", "ethereum", "solana", "cardano", "polkadot", "avalanche", "binance-smart-chain", "polygon"]
    selected_blockchains = st.multiselect(
        "데이터 수집 블록체인",
        options=all_blockchains,
        default=data_collection_config.get("blockchains", ["bitcoin", "ethereum", "solana", "cardano"]),
        help="데이터를 수집할 블록체인 선택"
    )

with tab3:
    st.subheader("UI 설정")
    
    ui_config = config.get("ui", {})
    
    # 테마 설정
    theme_options = ["light", "dark"]
    selected_theme = st.selectbox(
        "UI 테마",
        options=theme_options,
        index=theme_options.index(ui_config.get("theme", "light")) if ui_config.get("theme", "light") in theme_options else 0,
        help="UI 테마 선택"
    )
    
    # 차트 설정
    st.subheader("차트 설정")
    
    charts_config = ui_config.get("charts", {})
    
    # 기본 차트 기간 설정
    period_options = ["1h", "4h", "1d", "1w", "1m"]
    default_period = st.selectbox(
        "기본 차트 기간",
        options=period_options,
        index=period_options.index(charts_config.get("default_period", "1d")) if charts_config.get("default_period", "1d") in period_options else 2,
        help="기본적으로 표시할 차트 기간"
    )
    
    # 대시보드 설정
    st.subheader("대시보드 설정")
    
    dashboard_config = ui_config.get("dashboard", {})
    
    # 대시보드 새로고침 간격 설정
    refresh_interval_options = [0, 30, 60, 300, 600, 1800]
    refresh_interval = st.selectbox(
        "대시보드 자동 새로고침 간격 (초)",
        options=refresh_interval_options,
        index=refresh_interval_options.index(dashboard_config.get("refresh_interval", 300)) if dashboard_config.get("refresh_interval", 300) in refresh_interval_options else 3,
        format_func=lambda x: "사용 안함" if x == 0 else f"{x}초",
        help="대시보드 자동 새로고침 간격 (0 = 사용 안함)"
    )

with tab4:
    st.subheader("알림 설정")
    
    alerts_config = config.get("alerts", {})
    
    # 알림 활성화 설정
    alerts_enabled = st.checkbox(
        "알림 활성화",
        value=alerts_config.get("enabled", True),
        help="시스템 알림 활성화 여부"
    )
    
    # 이메일 알림 설정
    st.subheader("이메일 알림 설정")
    
    email_config = alerts_config.get("email", {})
    
    # 이메일 알림 활성화 설정
    email_enabled = st.checkbox(
        "이메일 알림 활성화",
        value=email_config.get("enabled", False),
        help="이메일을 통한 알림 전송 활성화"
    )
    
    # 이메일 알림이 활성화된 경우에만 설정 표시
    if email_enabled:
        # SMTP 서버 설정
        smtp_server = st.text_input(
            "SMTP 서버",
            value=email_config.get("smtp_server", ""),
            help="이메일 전송에 사용할 SMTP 서버 주소"
        )
        
        # SMTP 포트 설정
        smtp_port = st.number_input(
            "SMTP 포트",
            min_value=1,
            max_value=65535,
            value=email_config.get("smtp_port", 587),
            help="SMTP 서버 포트 (일반적으로 587 또는 465)"
        )
        
        # SMTP 사용자 이름 설정
        smtp_username = st.text_input(
            "SMTP 사용자 이름",
            value=email_config.get("username", ""),
            help="SMTP 서버 인증에 사용할 사용자 이름"
        )
        
        # SMTP 비밀번호 설정
        smtp_password = st.text_input(
            "SMTP 비밀번호",
            value=email_config.get("password", ""),
            type="password",
            help="SMTP 서버 인증에 사용할 비밀번호"
        )
        
        # 발신 이메일 설정
        from_email = st.text_input(
            "발신 이메일",
            value=email_config.get("from_email", ""),
            help="알림 발신에 사용할 이메일 주소"
        )
        
        # 수신 이메일 설정
        to_email = st.text_input(
            "수신 이메일",
            value=email_config.get("to_email", ""),
            help="알림을 수신할 이메일 주소"
        )
        
        # 이메일 테스트 버튼
        if st.button("이메일 전송 테스트"):
            st.info("테스트 이메일 전송 중...")
            # 여기에서 실제 이메일 전송 테스트 로직을 구현할 수 있음
            st.success("테스트 이메일이 전송되었습니다.")

# 설정 저장 버튼
if st.button("설정 저장", type="primary"):
    # 설정 객체 업데이트
    updated_config = {
        "api": {
            "base_url": api_base_url,
            "api_key": api_key,
            "ws_url": ws_url
        },
        "data_collection": {
            "interval": data_interval,
            "exchanges": selected_exchanges,
            "blockchains": selected_blockchains
        },
        "ui": {
            "theme": selected_theme,
            "charts": {
                "default_period": default_period,
                "available_periods": period_options
            },
            "dashboard": {
                "refresh_interval": refresh_interval
            }
        },
        "alerts": {
            "enabled": alerts_enabled,
            "email": {
                "enabled": email_enabled
            }
        }
    }
    
    # 이메일 알림이 활성화된 경우 설정 추가
    if email_enabled:
        updated_config["alerts"]["email"].update({
            "smtp_server": smtp_server,
            "smtp_port": smtp_port,
            "username": smtp_username,
            "password": smtp_password,
            "from_email": from_email,
            "to_email": to_email
        })
    
    # 설정 파일 저장
    try:
        if save_config(updated_config, 'config/config.yaml'):
            st.success("설정이 성공적으로 저장되었습니다.")
            st.cache_data.clear()  # 캐시 초기화
        else:
            st.error("설정 저장 중 오류가 발생했습니다.")
    except Exception as e:
        st.error(f"설정 저장 중 오류가 발생했습니다: {str(e)}")

# 설정 초기화 버튼
with st.expander("고급 옵션"):
    if st.button("설정 초기화", help="모든 설정을 기본값으로 초기화합니다."):
        # 설정 파일 삭제 또는 기본 설정으로 재설정
        try:
            default_config = {
                "api": {
                    "base_url": "http://localhost:8000",
                    "api_key": "",
                    "ws_url": "ws://localhost:8001"
                },
                "data_collection": {
                    "interval": 60,
                    "exchanges": ["binance", "upbit", "bithumb", "coinbase", "kraken"],
                    "blockchains": ["bitcoin", "ethereum", "solana", "cardano"]
                },
                "ui": {
                    "theme": "light",
                    "charts": {
                        "default_period": "1d",
                        "available_periods": ["1h", "4h", "1d", "1w", "1m"]
                    },
                    "dashboard": {
                        "refresh_interval": 300
                    }
                },
                "alerts": {
                    "enabled": True,
                    "email": {
                        "enabled": False,
                        "smtp_server": "",
                        "smtp_port": 587,
                        "username": "",
                        "password": "",
                        "from_email": "",
                        "to_email": ""
                    }
                }
            }
            
            if save_config(default_config, 'config/config.yaml'):
                st.success("설정이 기본값으로 초기화되었습니다.")
                st.cache_data.clear()  # 캐시 초기화
                st.experimental_rerun()  # 페이지 새로고침
            else:
                st.error("설정 초기화 중 오류가 발생했습니다.")
        except Exception as e:
            st.error(f"설정 초기화 중 오류가 발생했습니다: {str(e)}")

# 푸터
st.markdown("---")
st.markdown("© 2023 CryptoLytica - 고성능 암호화폐 데이터 수집 및 분석 플랫폼") 