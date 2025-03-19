import streamlit as st
import sys
import os
from pathlib import Path

# 루트 디렉토리 설정
ROOT_DIR = Path(__file__).parent
sys.path.append(str(ROOT_DIR))

# 코어 모듈 임포트
from core.app import get_page, run_app
from core.config import get_config_value

# 앱 설정
st.set_page_config(
    page_title="CryptoLytica - 암호화폐 분석 플랫폼",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 애플리케이션 실행
if __name__ == "__main__":
    run_app() 