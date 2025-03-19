import streamlit as st
import os
import importlib
import sys
from pathlib import Path
from typing import Dict, List, Callable

# 상위 디렉토리 경로 추가
ROOT_DIR = Path(__file__).parent.parent
sys.path.append(str(ROOT_DIR))

from core.config import load_config
from core.state import get_state, set_state

# 페이지 설정
st.set_page_config(
    page_title="CryptoLytica 관리자 UI",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 기본 정보
DOMAIN_PATH = "domains"
PAGES_DIR = "pages"

def discover_domains() -> List[str]:
    """사용 가능한 모든 도메인을 찾습니다."""
    domains_dir = ROOT_DIR / DOMAIN_PATH
    return [d.name for d in domains_dir.iterdir() if d.is_dir() and (d / PAGES_DIR).exists()]

def load_pages() -> Dict[str, Dict[str, Callable]]:
    """모든 도메인의 페이지를 동적으로 로드합니다."""
    domains = discover_domains()
    pages = {}
    
    for domain in domains:
        domain_pages = {}
        pages_dir = ROOT_DIR / DOMAIN_PATH / domain / PAGES_DIR
        
        if not pages_dir.exists():
            continue
            
        for page_file in pages_dir.glob("*.py"):
            if page_file.name == "__init__.py":
                continue
                
            # 모듈 경로 생성 (예: domains.blockchain.pages.blockchain_data)
            module_path = f"{DOMAIN_PATH}.{domain}.{PAGES_DIR}.{page_file.stem}"
            
            try:
                # 모듈 동적 로드
                module = importlib.import_module(module_path)
                
                # 페이지 타이틀과 함수 확인
                if hasattr(module, "page_title") and hasattr(module, "render_page"):
                    domain_pages[module.page_title] = module.render_page
                    
            except (ImportError, AttributeError) as e:
                st.error(f"페이지 로딩 오류: {module_path} - {str(e)}")
                
        if domain_pages:
            pages[domain] = domain_pages
            
    return pages

def main():
    """메인 애플리케이션 함수"""
    # 앱 헤더
    st.title("CryptoLytica 관리자 UI")
    
    # 설정 로드
    config = load_config()
    
    # 페이지 로드
    all_pages = load_pages()
    
    # 사이드바 네비게이션
    st.sidebar.title("네비게이션")
    
    # 도메인과 페이지 목록 준비
    domain_options = list(all_pages.keys())
    
    if not domain_options:
        st.warning("등록된 페이지가 없습니다. 도메인 디렉토리를 확인해주세요.")
        return
        
    # 도메인 선택
    selected_domain = st.sidebar.selectbox(
        "도메인 선택",
        options=domain_options
    )
    
    # 선택된 도메인의 페이지 목록
    domain_pages = all_pages.get(selected_domain, {})
    page_options = list(domain_pages.keys())
    
    if not page_options:
        st.warning(f"선택한 도메인 '{selected_domain}'에 페이지가 없습니다.")
        return
        
    # 페이지 선택
    selected_page = st.sidebar.selectbox(
        "페이지 선택",
        options=page_options
    )
    
    # 선택된 페이지 렌더링
    if selected_page in domain_pages:
        # 페이지 상태 저장
        set_state("current_domain", selected_domain)
        set_state("current_page", selected_page)
        
        # 페이지 렌더링
        domain_pages[selected_page]()
    else:
        st.error(f"페이지를 찾을 수 없습니다: {selected_page}")
    
    # 푸터
    st.markdown("---")
    st.markdown("© 2023 CryptoLytica - 고성능 암호화폐 데이터 수집 및 분석 플랫폼")

if __name__ == "__main__":
    main() 