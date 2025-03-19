# CryptoLytica UI

CryptoLytica UI는 암호화폐 데이터 분석 및 시각화를 위한 웹 기반 인터페이스입니다.

## 주요 기능

- **블록체인 데이터 분석**: 트랜잭션 통계, 지갑 활동, 스마트 컨트랙트 활동 분석
- **포트폴리오 분석**: 자산 배분, 성과 추적, 위험 분석
- **시장 분석**: 가격 차트, 시장 지표, 거래소 데이터 분석
- **거래소 데이터**: 주문, 거래 볼륨, 시장 깊이 분석

## 기술 스택

- **프론트엔드**: Streamlit을 활용한 인터랙티브 대시보드
- **데이터 시각화**: Plotly, Pandas
- **API 통신**: REST API, WebSocket
- **분석 라이브러리**: NumPy, SciPy, TA-Lib

## 프로젝트 구조

```
cryptolytica_ui/
├── core/                   # 핵심 앱 코드
│   ├── app.py              # 메인 앱 로직
│   ├── config.py           # 설정 관리
│   └── state.py            # 상태 관리
├── domains/                # 도메인별 코드
│   ├── blockchain/         # 블록체인 도메인
│   │   ├── pages/          # 블록체인 페이지
│   │   ├── models/         # 블록체인 데이터 모델
│   │   ├── services/       # 블록체인 서비스
│   │   └── utils/          # 블록체인 유틸리티
│   ├── portfolio/          # 포트폴리오 도메인
│   ├── market/             # 시장 분석 도메인
│   ├── exchange/           # 거래소 도메인
│   └── dashboard/          # 대시보드 도메인
├── shared/                 # 공유 리소스
│   ├── components/         # 공유 UI 컴포넌트
│   ├── models/             # 공유 데이터 모델
│   ├── services/           # 공유 서비스 
│   └── utils/              # 공유 유틸리티
├── config/                 # 설정 파일
│   └── config.yaml         # 기본 설정
├── main.py                 # 엔트리 포인트
├── requirements.txt        # 패키지 의존성
└── README.md               # 프로젝트 설명
```

## Factor-12 설계 원칙

이 프로젝트는 Factor-12 원칙을 기반으로 설계되었습니다:

1. **도메인 분리**: 각 도메인(블록체인, 포트폴리오, 시장, 거래소)은 완전히 독립적
2. **단일 책임**: 각 클래스와 함수는 하나의 책임만 가짐
3. **인터페이스 분리**: 클라이언트는 사용하지 않는 인터페이스에 의존하지 않음
4. **의존성 주입**: 외부 의존성은 생성자나 함수 매개변수를 통해 주입
5. **캡슐화**: 구현 세부 사항은 숨기고 명확한 인터페이스만 공개
6. **느슨한 결합**: 컴포넌트 간 최소한의 지식만 공유
7. **확장성 우선**: 기존 코드 수정보다 확장을 통한 기능 추가
8. **상태 관리**: 전역 상태는 피하고 명시적인 상태 관리
9. **테스트 용이성**: 모든 코드는 테스트 가능하도록 설계
10. **일관된 추상화**: 적절한 추상화 수준 유지
11. **재사용 가능성**: 공통 기능은 공유 모듈로 분리
12. **명확한 인터페이스**: 각 도메인 간 통신은 명확하게 정의된 인터페이스로만 가능

## 설치 및 실행

1. 환경 설정:
   ```bash
   python -m venv venv
   source venv/bin/activate  # Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

2. 환경 변수 설정:
   ```bash
   cp .env.example .env
   # .env 파일을 수정하여 필요한 설정 입력
   ```

3. 애플리케이션 실행:
   ```bash
   python main.py
   # 또는
   streamlit run main.py
   ```

## 개발 가이드

### 새 도메인 추가

새 도메인을 추가하려면:

1. `domains/` 아래에 새 도메인 폴더 생성
2. 도메인에 필요한 `pages/`, `models/`, `services/`, `utils/` 폴더 생성
3. 각 페이지 모듈에 `page_title`과 `render_page()` 함수 구현

### 페이지 개발

각 페이지 모듈은 다음 구조를 따라야 합니다:

```python
# domains/example/pages/example_page.py

import streamlit as st

# 페이지 타이틀 (필수)
page_title = "예시 페이지"

# 페이지 렌더링 함수 (필수)
def render_page():
    st.title("예시 페이지")
    # 페이지 내용 구현
```

## 라이선스

이 프로젝트는 MIT 라이선스 하에 배포됩니다.

## 기여

기여는 언제나 환영합니다! 다음 과정을 따라주세요:

1. 이슈 생성 또는 기존 이슈 선택
2. 브랜치 생성 (`feature/issue-번호-설명`)
3. 변경사항 커밋
4. Pull Request 제출 