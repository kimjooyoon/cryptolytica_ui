import streamlit as st
import os
import yaml
from dotenv import load_dotenv

# 환경 변수 로드
load_dotenv()

# 설정 파일 로드
@st.cache_data
def load_config():
    try:
        with open('config/config.yaml', 'r') as file:
            return yaml.safe_load(file)
    except FileNotFoundError:
        return {
            "api": {
                "base_url": os.getenv("API_BASE_URL", "http://localhost:8000"),
                "api_key": os.getenv("API_KEY", "")
            }
        }

# 페이지 설정
st.set_page_config(
    page_title="CryptoLytica 관리자 UI",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 앱 헤더
st.title("CryptoLytica 관리자 UI")

# 사이드바
st.sidebar.title("네비게이션")
page = st.sidebar.radio(
    "페이지 선택",
    ["대시보드", "거래소 데이터", "블록체인 데이터", "포트폴리오 분석", "시장 분석", "설정"]
)

# 설정 로드
config = load_config()

# 페이지 표시
if page == "대시보드":
    st.header("대시보드")
    
    # 대시보드 레이아웃
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("시스템 상태")
        st.metric(label="API 서버", value="온라인", delta="정상")
        st.metric(label="데이터 수집기", value="실행 중", delta="정상")
        st.metric(label="최근 업데이트", value="10분 전")
    
    with col2:
        st.subheader("주요 지표")
        st.metric(label="수집된 거래소", value="5", delta="2 추가")
        st.metric(label="처리된 트랜잭션", value="1.2M", delta="100K 증가")
        st.metric(label="저장 공간 사용", value="250GB", delta="10GB 증가")
    
    # 가상의 차트
    st.subheader("시스템 성능")
    chart_data = {
        "시간": ["00:00", "06:00", "12:00", "18:00", "현재"],
        "CPU 사용률": [30, 45, 60, 40, 35],
        "메모리 사용률": [45, 55, 70, 60, 50],
        "API 요청": [100, 150, 300, 250, 200]
    }
    
    st.line_chart(chart_data, x="시간")
    
    # 최근 이벤트
    st.subheader("최근 이벤트")
    st.table({
        "시간": ["08:15", "07:30", "06:45", "05:20", "04:10"],
        "이벤트": [
            "바이낸스 데이터 수집 완료",
            "BTC 온체인 분석 업데이트",
            "시스템 백업 완료",
            "Upbit API 연결 문제 해결됨",
            "이더리움 데이터 피드 재시작"
        ],
        "상태": ["성공", "성공", "성공", "경고", "성공"]
    })

elif page == "거래소 데이터":
    st.header("거래소 데이터")
    st.info("이 페이지는 현재 개발 중입니다.")

elif page == "블록체인 데이터":
    st.header("블록체인 데이터")
    st.info("이 페이지는 현재 개발 중입니다.")

elif page == "포트폴리오 분석":
    st.header("포트폴리오 분석")
    st.info("이 페이지는 현재 개발 중입니다.")

elif page == "시장 분석":
    st.header("시장 분석")
    st.info("이 페이지는 현재 개발 중입니다.")

elif page == "설정":
    st.header("설정")
    
    # API 설정
    st.subheader("API 설정")
    api_url = st.text_input("API 기본 URL", value=config["api"]["base_url"])
    api_key = st.text_input("API 키", value=config["api"]["api_key"], type="password")
    
    if st.button("설정 저장"):
        # 여기서 설정을 저장하는 로직을 구현
        st.success("설정이 저장되었습니다!")

# 푸터
st.markdown("---")
st.markdown("© 2023 CryptoLytica - 고성능 암호화폐 데이터 수집 및 분석 플랫폼") 