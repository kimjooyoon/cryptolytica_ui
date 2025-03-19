# 도메인 중심 구조 마이그레이션 가이드

이 문서는 CryptoLytica UI 프로젝트의 레거시 페이지 기반 구조에서 새로운 도메인 중심 구조로 마이그레이션하는 과정을 안내합니다.

## 마이그레이션 개요

프로젝트는 점진적으로 기존 페이지 기반 구조에서 도메인 중심 구조로 마이그레이션하고 있습니다. 이 과정에서 기존 코드는 계속 작동하면서 새로운 구조로 점진적으로 이전됩니다.

## 마이그레이션 상태

| 도메인 | 마이그레이션 상태 | 완료 날짜 |
|-------|----------------|----------|
| blockchain | 완료 | 2023-03-19 |
| exchange | 진행 중 | - |
| portfolio | 계획됨 | - |
| market | 계획됨 | - |
| dashboard | 구조만 생성됨 | - |

## 마이그레이션 단계

각 페이지의 마이그레이션은 다음 단계를 따릅니다:

### 1. 도메인 구조 설정

```bash
mkdir -p domains/<domain_name>/models
mkdir -p domains/<domain_name>/services
mkdir -p domains/<domain_name>/utils
mkdir -p domains/<domain_name>/views
touch domains/<domain_name>/__init__.py
touch domains/<domain_name>/models/__init__.py
touch domains/<domain_name>/services/__init__.py
touch domains/<domain_name>/utils/__init__.py
touch domains/<domain_name>/views/__init__.py
```

### 2. 데이터 모델 분리

1. 기존 페이지에서 데이터 구조를 식별합니다.
2. 이를 데이터클래스 또는 클래스로 모델화합니다.
3. 타입 힌트와 문서화를 추가합니다.

예시:
```python
"""
도메인 데이터 모델 정의
"""
from dataclasses import dataclass
from datetime import datetime
from typing import List, Dict, Optional, Any

@dataclass
class SomeModel:
    """모델에 대한 설명"""
    id: str
    name: str
    created_at: datetime
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'SomeModel':
        """딕셔너리에서 모델 생성"""
        return cls(
            id=data["id"],
            name=data["name"],
            created_at=datetime.fromisoformat(data["created_at"].replace('Z', '+00:00'))
        )
```

### 3. 서비스 레이어 분리

1. 기존 페이지에서 API 호출 및 데이터 처리 로직을 식별합니다.
2. 이를 서비스 클래스로 분리합니다.
3. 모델을 사용하여 데이터 타입을 명확히 합니다.

예시:
```python
"""
도메인 서비스 구현
"""
from typing import List, Dict, Any
from api.client import CryptoLyticaClient
from domains.some_domain.models.some_model import SomeModel

class SomeService:
    """서비스 클래스 설명"""
    
    def __init__(self, client: CryptoLyticaClient):
        self.client = client
    
    def get_some_data(self) -> List[SomeModel]:
        """데이터 가져오기"""
        raw_data = self.client.get_some_data()
        return [SomeModel.from_dict(item) for item in raw_data]
```

### 4. 유틸리티 함수 분리

1. 기존 페이지에서 특정 도메인에 관련된 유틸리티 함수를 식별합니다.
2. 이를 유틸리티 모듈로 분리합니다.

예시:
```python
"""
도메인 유틸리티 함수
"""
from typing import Dict, Any

def format_some_data(data: Dict[str, Any]) -> str:
    """데이터 포맷팅"""
    # 구현
    return formatted_result
```

### 5. 뷰 레이어 분리

1. 기존 페이지에서 UI 렌더링 코드를 식별합니다.
2. 이를 뷰 모듈로 분리하고 서비스를 주입합니다.

예시:
```python
"""
도메인 UI 컴포넌트
"""
import streamlit as st
from domains.some_domain.services.some_service import SomeService

def render_some_view():
    """UI 렌더링"""
    st.title("도메인 뷰")
    
    # 서비스 초기화 및 사용
    client = get_api_client()
    service = SomeService(client)
    
    # 데이터 가져오기
    data = service.get_some_data()
    
    # UI 렌더링
    for item in data:
        st.write(f"이름: {item.name}")
```

### 6. 새로운 페이지 생성

1. 도메인 뷰를 사용하는 새 페이지 파일을 생성합니다.
2. 기존 페이지는 유지하여 호환성을 보장합니다.

예시:
```python
"""
새로운 도메인 구조를 사용하는 페이지
"""
from domains.some_domain.views.some_view import render_some_view

# 도메인 뷰 렌더링
render_some_view()
```

### 7. 테스트 및 배포

1. 새 구조가 기존 기능과 동일하게 작동하는지 테스트합니다.
2. 문제가 없으면 변경 사항을 배포합니다.

## 모범 사례

마이그레이션 과정에서 다음 모범 사례를 따르세요:

1. **타입 힌트 사용**: 모든 함수와 클래스에 타입 힌트를 추가하세요.
2. **문서화**: 모듈, 클래스, 함수에 독스트링을 추가하세요.
3. **점진적 마이그레이션**: 한 번에 모든 것을 변경하지 말고 도메인별로 점진적으로 마이그레이션하세요.
4. **테스트**: 마이그레이션 후 새 구조가 기존 기능과 동일하게 작동하는지 테스트하세요.
5. **README 작성**: 각 도메인에 대한 README.md를 작성하여 사용 방법과 구조를 문서화하세요. 