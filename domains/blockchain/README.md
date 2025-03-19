# 블록체인 도메인

블록체인 도메인은 다양한 블록체인 네트워크의 데이터를 조회, 분석 및 시각화하는 기능을 담당합니다.

## 구조

```
blockchain/
├── models/                 # 데이터 모델
│   ├── __init__.py         
│   └── blockchain_model.py # 블록체인 관련 데이터 모델
├── services/               # 비즈니스 로직
│   ├── __init__.py
│   └── blockchain_service.py # 블록체인 데이터 처리 서비스
├── utils/                  # 유틸리티 함수
│   ├── __init__.py
│   └── blockchain_utils.py # 블록체인 특화 유틸리티
├── views/                  # UI 컴포넌트
│   ├── __init__.py
│   └── blockchain_view.py  # 블록체인 데이터 시각화 컴포넌트
└── __init__.py             # 패키지 초기화
```

## 주요 기능

이 도메인은 다음과 같은 주요 기능을 제공합니다:

1. **블록체인 데이터 조회**
   - 블록체인 목록 및 상태 정보 조회
   - 블록체인별 트랜잭션 통계 조회

2. **트랜잭션 분석**
   - 시간별 트랜잭션 수 분석
   - 평균 수수료 추이 분석
   - 블록 크기 및 활성 주소 분석

3. **지갑 활동 분석**
   - 주요 지갑의 활동 조회
   - 지갑 활동 유형 분류 및 분석

4. **스마트 컨트랙트 활동**
   - 스마트 컨트랙트 활동 모니터링
   - 컨트랙트 활동의 유형별 분포 분석
   - 트랜잭션 및 사용자 분석

## 사용 방법

새로운 도메인 구조를 사용하는 페이지:

```python
from domains.blockchain.views.blockchain_view import render_blockchain_view

# 블록체인 뷰 렌더링
render_blockchain_view()
```

블록체인 서비스만 직접 사용하는 예:

```python
from api.client import CryptoLyticaClient
from domains.blockchain.services.blockchain_service import BlockchainService

client = CryptoLyticaClient(...)
blockchain_service = BlockchainService(client)

# 블록체인 목록 가져오기
blockchains = blockchain_service.get_blockchains()

# 트랜잭션 데이터 가져오기
transactions = blockchain_service.get_blockchain_transactions("bitcoin", limit=100)
```

## 리팩토링 노트

이 도메인은 `pages/blockchain_data.py`에서 리팩토링되었습니다. 리팩토링 과정에서 다음과 같은 변경 사항이 적용되었습니다:

1. **코드 분리**
   - 데이터 모델, 서비스, 유틸리티 및 뷰 레이어로 코드 분리
   - UI 렌더링 로직과 비즈니스 로직의 명확한 구분

2. **타입 힌트 추가**
   - 모든 함수와 클래스에 Python 타입 힌트 추가
   - 데이터 구조를 명확하게 정의하는 데이터클래스 사용

3. **에러 처리 개선**
   - 예외 처리 추가
   - 사용자에게 친숙한 오류 메시지 표시

4. **문서화 향상**
   - 각 모듈, 클래스 및 함수에 독스트링 추가
   - 도메인 전용 README.md 파일 작성 