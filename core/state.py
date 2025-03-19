import streamlit as st
from typing import Any, Dict, Optional

# 상태 저장소 초기화
def init_state() -> None:
    """앱 상태를 초기화합니다."""
    if "app_state" not in st.session_state:
        st.session_state.app_state = {}

# 상태 설정
def set_state(key: str, value: Any) -> None:
    """특정 키의 앱 상태를 설정합니다."""
    init_state()
    st.session_state.app_state[key] = value

# 상태 가져오기
def get_state(key: str, default: Any = None) -> Any:
    """특정 키의 앱 상태를 가져옵니다."""
    init_state()
    return st.session_state.app_state.get(key, default)

# 여러 상태 설정
def set_multiple_states(states: Dict[str, Any]) -> None:
    """여러 키의 앱 상태를 한 번에 설정합니다."""
    init_state()
    for key, value in states.items():
        st.session_state.app_state[key] = value

# 도메인별 상태 관리
def get_domain_state(domain: str, key: str, default: Any = None) -> Any:
    """특정 도메인의 상태 값을 가져옵니다."""
    domain_key = f"{domain}:{key}"
    return get_state(domain_key, default)

def set_domain_state(domain: str, key: str, value: Any) -> None:
    """특정 도메인의 상태 값을 설정합니다."""
    domain_key = f"{domain}:{key}"
    set_state(domain_key, value)

# 페이지별 상태 관리
def get_page_state(domain: str, page: str, key: str, default: Any = None) -> Any:
    """특정 페이지의 상태 값을 가져옵니다."""
    page_key = f"{domain}:{page}:{key}"
    return get_state(page_key, default)

def set_page_state(domain: str, page: str, key: str, value: Any) -> None:
    """특정 페이지의 상태 값을 설정합니다."""
    page_key = f"{domain}:{page}:{key}"
    set_state(page_key, value)

# 현재 도메인/페이지 상태 관리
def get_current_domain() -> Optional[str]:
    """현재 선택된 도메인을 가져옵니다."""
    return get_state("current_domain")

def get_current_page() -> Optional[str]:
    """현재 선택된 페이지를 가져옵니다."""
    return get_state("current_page")

# 앱 전체 상태 초기화
def reset_state() -> None:
    """앱 상태를 완전히 초기화합니다."""
    if "app_state" in st.session_state:
        st.session_state.app_state = {} 