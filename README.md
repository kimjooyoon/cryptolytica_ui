# CryptoLytica 관리자 UI

CryptoLytica 프로젝트를 위한 Streamlit 기반 관리자 UI입니다. 이 UI는 암호화폐 데이터 수집 및 분석 플랫폼인 CryptoLytica의 데이터를 시각화하고 관리하는 기능을 제공합니다.

## 주요 기능

- 다중 거래소 데이터 시각화
- 블록체인 온체인 데이터 분석
- 포트폴리오 분석 및 최적화
- 시장 분석 및 패턴 인식
- 시스템 상태 모니터링 및 관리

## 설치 방법

```bash
# 저장소 클론
git clone https://github.com/yourusername/cryptolytica_ui.git
cd cryptolytica_ui

# 의존성 설치
pip install -r requirements.txt

# 환경 변수 설정 (필요시)
cp .env.example .env
# .env 파일 편집

# 애플리케이션 실행
streamlit run app.py
```

## 프로젝트 구조

```
cryptolytica_ui/
├── app.py                     # 메인 Streamlit 애플리케이션
├── requirements.txt           # 의존성 패키지 목록
├── config/                    # 설정 파일
│   └── config.yaml            # API 엔드포인트, 인증 정보 등 설정
├── pages/                     # 페이지별 Streamlit 스크립트
│   ├── dashboard.py           # 메인 대시보드
│   ├── exchange_data.py       # 거래소 데이터 분석
│   ├── blockchain_data.py     # 블록체인 데이터 분석
│   ├── portfolio.py           # 포트폴리오 분석
│   ├── market_analysis.py     # 시장 분석
│   └── settings.py            # 시스템 설정
├── api/                       # API 연동 모듈
│   ├── client.py              # CryptoLytica API 클라이언트
│   └── models.py              # 데이터 모델
└── utils/                     # 유틸리티 함수
    ├── visualization.py       # 차트 및 시각화 도구
    └── helpers.py             # 헬퍼 함수
```

## 사용 방법

1. 애플리케이션을 실행합니다: `streamlit run app.py`
2. 웹 브라우저에서 http://localhost:8501 접속
3. 사이드바에서 원하는 기능 선택

## 환경 설정

`config/config.yaml` 파일을 통해 API 엔드포인트, 인증 정보 등을 설정할 수 있습니다. 또는 `.env` 파일을 통해 환경 변수를 설정할 수도 있습니다.

## 라이센스

이 프로젝트는 Apache License 2.0 라이센스 하에 배포됩니다. 