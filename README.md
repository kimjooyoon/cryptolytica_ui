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

### 기존 구조
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
│   └── settings.py            # 시스템 설정
├── api/                       # API 연동 모듈
│   ├── client.py              # CryptoLytica API 클라이언트
│   └── models.py              # 데이터 모델
└── utils/                     # 유틸리티 함수
    ├── visualization.py       # 차트 및 시각화 도구
    └── helpers.py             # 헬퍼 함수
```

### 새로운 도메인 중심 구조
```
cryptolytica_ui/
├── app.py                     # 메인 Streamlit 애플리케이션
├── requirements.txt           # 의존성 패키지 목록
├── config/                    # 설정 파일
│   └── config.yaml            # API 엔드포인트, 인증 정보 등 설정
├── domains/                   # 도메인 중심 구조
│   ├── blockchain/            # 블록체인 도메인
│   │   ├── models/            # 데이터 모델
│   │   ├── services/          # 비즈니스 로직
│   │   ├── utils/             # 도메인별 유틸리티
│   │   └── views/             # UI 컴포넌트
│   ├── exchange/              # 거래소 도메인
│   ├── portfolio/             # 포트폴리오 도메인
│   ├── market/                # 시장 분석 도메인
│   └── dashboard/             # 대시보드 도메인
├── shared/                    # 공유 컴포넌트
│   └── components/            # 공유 UI 컴포넌트
├── pages/                     # 레거시 페이지 (점진적 마이그레이션)
├── api/                       # 레거시 API 클라이언트 (점진적 마이그레이션)
└── utils/                     # 공통 유틸리티 함수
```

> 📊 **구조 시각화**: 프로젝트 구조와 도메인 관계의 시각적 표현은 [domains/VISUALIZATION.md](domains/VISUALIZATION.md) 문서를 참조하세요.
> 🔄 **마이그레이션 가이드**: 도메인 중심 구조로의 마이그레이션 방법은 [domains/MIGRATION.md](domains/MIGRATION.md) 문서를 참조하세요.

## 도메인 중심 구조 설명

프로젝트는 점진적으로 페이지 기반 구조에서 도메인 중심 구조로 마이그레이션하고 있습니다. 도메인 중심 구조는 다음과 같은 장점을 제공합니다:

1. **관심사 분리**: 각 도메인은 자체 모델, 서비스, 유틸리티 및 뷰를 가집니다.
2. **재사용성 향상**: 도메인별 모듈은 명확한 책임과 경계를 갖습니다.
3. **유지보수성 개선**: 관련 코드가 함께 위치하여 유지보수가 용이합니다.
4. **확장성 증대**: 새로운 기능을 추가할 때 기존 구조를 쉽게 확장할 수 있습니다.

### 도메인 구조 세부 설명

각 도메인은 다음과 같은 구조를 따릅니다:

- **models/**: 데이터 모델 및 스키마 정의
- **services/**: 비즈니스 로직 및 데이터 처리
- **utils/**: 도메인별 유틸리티 함수
- **views/**: UI 컴포넌트 및 렌더링 로직

## 리팩토링 가이드

기존 페이지 기반 코드를 도메인 중심 구조로 리팩토링하는 과정은 다음과 같습니다:

1. **도메인 식별**: 페이지의 주요 기능과 관련된 도메인을 식별합니다.
2. **도메인 구조 생성**: 필요한 디렉토리 구조를 생성합니다.
3. **코드 분리**: 기존 페이지 코드를 다음과 같이 분리합니다:
   - 데이터 모델 -> models/
   - 비즈니스 로직 -> services/
   - 유틸리티 함수 -> utils/
   - UI 컴포넌트 -> views/
4. **새 페이지 생성**: 도메인 구조를 이용하는 새 페이지를 생성합니다.
5. **테스트 및 검증**: 새 구조가 기존 기능과 동일하게 작동하는지 확인합니다.

## 사용 방법

1. 애플리케이션을 실행합니다: `streamlit run app.py`
2. 웹 브라우저에서 http://localhost:8501 접속
3. 사이드바에서 원하는 기능 선택

## 환경 설정

`config/config.yaml` 파일을 통해 API 엔드포인트, 인증 정보 등을 설정할 수 있습니다. 또는 `.env` 파일을 통해 환경 변수를 설정할 수도 있습니다.

## 라이센스

이 프로젝트는 Apache License 2.0 라이센스 하에 배포됩니다. 