import os
import yaml
import streamlit as st
from pathlib import Path
from typing import Dict, Any
from dotenv import load_dotenv

# 환경 변수 로드
load_dotenv()

# 기본 경로 설정
ROOT_DIR = Path(__file__).parent.parent
CONFIG_FILE = ROOT_DIR / "config" / "config.yaml"

@st.cache_data(ttl=300)
def load_config() -> Dict[str, Any]:
    """설정 파일을 로드합니다."""
    try:
        if CONFIG_FILE.exists():
            with open(CONFIG_FILE, 'r') as file:
                config = yaml.safe_load(file)
        else:
            # 기본 설정
            config = create_default_config()
            
        # 환경 변수로 설정 재정의
        override_config_from_env(config)
        return config
    except Exception as e:
        st.error(f"설정 로드 중 오류 발생: {str(e)}")
        return create_default_config()

def override_config_from_env(config: Dict[str, Any]) -> None:
    """환경 변수에서 설정을 재정의합니다."""
    # API 기본 URL
    if os.getenv("API_BASE_URL"):
        if "api" not in config:
            config["api"] = {}
        config["api"]["base_url"] = os.getenv("API_BASE_URL")
    
    # API 키
    if os.getenv("API_KEY"):
        if "api" not in config:
            config["api"] = {}
        config["api"]["api_key"] = os.getenv("API_KEY")
    
    # WebSocket URL
    if os.getenv("WS_URL"):
        if "api" not in config:
            config["api"] = {}
        config["api"]["ws_url"] = os.getenv("WS_URL")

def create_default_config() -> Dict[str, Any]:
    """기본 설정을 생성합니다."""
    return {
        "api": {
            "base_url": os.getenv("API_BASE_URL", "http://localhost:8000"),
            "api_key": os.getenv("API_KEY", ""),
            "ws_url": os.getenv("WS_URL", "ws://localhost:8001")
        },
        "app": {
            "theme": "light",
            "language": "ko",
            "cache_ttl": 300
        },
        "features": {
            "real_time_updates": True,
            "notifications": True,
            "data_export": True
        }
    }

def save_config(config: Dict[str, Any]) -> bool:
    """설정을 파일에 저장합니다."""
    try:
        # 설정 파일 디렉토리 생성
        os.makedirs(os.path.dirname(CONFIG_FILE), exist_ok=True)
        
        # 설정 파일 저장
        with open(CONFIG_FILE, 'w') as file:
            yaml.dump(config, file, default_flow_style=False)
        return True
    except Exception as e:
        st.error(f"설정 저장 중 오류 발생: {str(e)}")
        return False

def get_config_value(key_path: str, default: Any = None) -> Any:
    """
    점으로 구분된 경로를 사용하여 설정 값을 가져옵니다.
    예: get_config_value("api.base_url")
    """
    config = load_config()
    keys = key_path.split('.')
    
    # 재귀적으로 설정 값 찾기
    current = config
    for key in keys:
        if isinstance(current, dict) and key in current:
            current = current[key]
        else:
            return default
    
    return current 