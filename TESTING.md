# 테스트 실행 가이드

## 빠른 시작

```bash
# 1. 의존성 설치
make install
make install-playwright

# 2. 전체 테스트 실행
make test

# 3. TDD 모드 (자동 재실행)
make test-watch
```

---

## 테스트 유형

### 1. 단위 테스트 (Unit Tests)

**위치:** `jellserver/tests/`

**실행:**
```bash
make test-unit
# 또는
pytest jellserver/tests/
```

**특징:**
- 빠른 실행 속도
- 개별 함수/메서드 테스트
- 데이터베이스 사용

**예제:**
```python
# jellserver/tests/test_models.py
@pytest.mark.django_db
def test_post_creation():
    post = PostFactory()
    assert post.id is not None
```

---

### 2. 통합 테스트 (Integration Tests)

**위치:** `tests/integration/`

**실행:**
```bash
make test-integration
# 또는
pytest tests/integration/
```

**특징:**
- 여러 컴포넌트 간 상호작용 테스트
- 데이터베이스, API, Serializer 통합
- 중간 속도

**예제:**
```python
# tests/integration/test_post_integration.py
@pytest.mark.django_db
def test_create_retrieve_workflow():
    # Create
    response = client.post('/api/post/', data)
    # Retrieve
    response = client.get(f'/api/post/{post_id}/')
    # Assert
    assert response.status_code == 200
```

---

### 3. E2E 테스트 (End-to-End Tests)

**위치:** `tests/e2e/`

#### 3.1 API E2E 테스트

**실행:**
```bash
pytest tests/e2e/test_api_e2e.py
```

**특징:**
- 실제 HTTP 요청
- 전체 스택 테스트 (DB → API → Response)
- httpx 사용

**예제:**
```python
# tests/e2e/test_api_e2e.py
def test_create_post_e2e(live_server):
    with httpx.Client() as client:
        response = client.post(
            f"{live_server.url}/api/post/",
            json={'title': 'E2E', ...}
        )
        assert response.status_code == 201
```

#### 3.2 브라우저 E2E 테스트

**실행:**
```bash
make test-e2e
# 또는
pytest tests/e2e/test_browser_e2e.py
```

**브라우저를 보면서 실행:**
```bash
make test-e2e-headed
# 또는
pytest tests/e2e/ --headed
```

**특징:**
- 실제 브라우저 자동화
- Playwright 사용
- 사용자 워크플로우 테스트

**예제:**
```python
# tests/e2e/test_browser_e2e.py
def test_admin_login(page: Page, live_server):
    page.goto(f"{live_server.url}/admin/")
    page.fill('input[name="username"]', 'admin')
    page.fill('input[name="password"]', 'admin123')
    page.click('input[type="submit"]')
    expect(page.locator('body')).to_contain_text('Site administration')
```

---

## 일반 테스트 명령어

### 전체 테스트
```bash
make test                # 모든 테스트
make test-parallel       # 병렬 실행 (빠름)
```

### 커버리지
```bash
make test-cov            # 커버리지 리포트 생성
open htmlcov/index.html  # 리포트 보기
```

### TDD 모드
```bash
make test-watch          # 파일 변경 시 자동 실행
make tdd                 # 위와 동일
```

### 실패한 테스트만 재실행
```bash
make test-failed
# 또는
pytest --lf
```

---

## 고급 사용법

### 특정 테스트 파일만 실행
```bash
pytest jellserver/tests/test_models.py
```

### 특정 테스트 함수만 실행
```bash
pytest jellserver/tests/test_models.py::test_post_creation
```

### 키워드로 필터링
```bash
pytest -k "post"         # 이름에 'post' 포함
pytest -k "not e2e"      # E2E 제외
```

### 마커로 필터링
```bash
pytest -m "django_db"    # django_db 마커만
pytest -m "not slow"     # slow 마커 제외
pytest -m "integration"  # 통합 테스트만
```

### 상세 출력
```bash
pytest -v                # Verbose
pytest -vv               # 더 상세
pytest -s                # print 출력 표시
```

### 특정 브라우저로 E2E 실행
```bash
pytest tests/e2e/ --browser chromium
pytest tests/e2e/ --browser firefox
pytest tests/e2e/ --browser webkit
```

### 병렬 실행
```bash
pytest -n 4              # 4개 프로세스
pytest -n auto           # CPU 코어 수만큼
```

### 실패 시 즉시 중단
```bash
pytest -x                # 첫 실패 시 중단
pytest --maxfail=3       # 3번 실패 시 중단
```

---

## 환경별 테스트

### 로컬 개발 환경
```bash
# 기본 테스트
make test

# TDD 모드로 개발
make test-watch
```

### CI/CD 환경
```bash
# GitHub Actions에서 자동 실행
# .github/workflows/ci.yml 참조

# 로컬에서 CI처럼 실행
make ci
```

### Docker 환경
```bash
# Docker Compose로 테스트
docker-compose exec web pytest

# 모든 서비스와 함께 테스트
docker-compose run --rm web pytest
```

---

## 테스트 데이터 생성

### Factory 사용
```python
from jellserver.tests.factories import PostFactory

# 기본 생성
post = PostFactory()

# 특정 값 지정
post = PostFactory(title='특정 제목', div='notice')

# 여러 개 생성
posts = PostFactory.create_batch(10)

# 특정 타입
notice = NoticePostFactory()
deleted = DeletedPostFactory()
```

### Faker 사용
```python
from faker import Faker

fake = Faker('ko_KR')

title = fake.sentence()
content = fake.paragraph()
name = fake.name()
```

---

## 디버깅

### PDB 사용
```bash
# 테스트 중 중단점
pytest -s --pdb

# 실패 시 PDB 시작
pytest --pdb
```

### 특정 테스트만 디버깅
```python
# 테스트 코드에 추가
import pdb; pdb.set_trace()

# 또는
breakpoint()  # Python 3.7+
```

### 로그 출력
```bash
# 모든 로그 표시
pytest -s --log-cli-level=DEBUG

# 특정 레벨만
pytest --log-cli-level=INFO
```

---

## 성능 측정

### 가장 느린 테스트 찾기
```bash
pytest --durations=10    # 상위 10개
pytest --durations=0     # 전체
```

### 프로파일링
```bash
pytest --profile
```

---

## CI/CD 통합

### GitHub Actions

`.github/workflows/ci.yml`에서 자동 실행:

```yaml
- Unit & Integration Tests
- E2E Tests (Playwright)
- Coverage Report
- Security Checks
```

### Pre-commit Hooks

```bash
# 설치
pip install pre-commit
pre-commit install

# 커밋 전 자동 실행:
# - 코드 포맷팅
# - 린팅
# - 간단한 테스트 (optional)
```

---

## 트러블슈팅

### Playwright 브라우저 설치 안됨
```bash
playwright install --with-deps chromium
```

### 테스트 데이터베이스 에러
```bash
# 테스트 DB 초기화
python manage.py migrate --run-syncdb

# 또는 pytest 옵션
pytest --create-db
```

### 느린 테스트
```bash
# 병렬 실행
pytest -n auto

# 또는 특정 테스트만
pytest -k "not slow"
```

### 임포트 에러
```bash
# Python path 확인
export PYTHONPATH=/path/to/django_server:$PYTHONPATH

# 또는 개발 모드 설치
pip install -e .
```

---

## 모범 사례

### ✅ DO

1. **TDD 모드로 개발**
   ```bash
   make test-watch
   ```

2. **커밋 전 테스트 실행**
   ```bash
   make test
   ```

3. **의미 있는 테스트 이름**
   ```python
   def test_deleted_posts_excluded_from_list():
       pass
   ```

4. **Factory 사용**
   ```python
   post = PostFactory()  # ✅
   # not Post.objects.create(...)  # ❌
   ```

### ❌ DON'T

1. **테스트 건너뛰지 말기**
   ```python
   @pytest.mark.skip  # ❌ 피하기
   ```

2. **테스트 간 의존성**
   ```python
   # ❌ Bad
   def test_a():
       global data
       data = create_data()

   def test_b():
       use(data)  # test_a에 의존
   ```

3. **실제 외부 API 호출**
   ```python
   # ❌ Bad: 실제 API 호출
   response = requests.get('https://real-api.com')

   # ✅ Good: Mock 사용
   @patch('myapp.requests.get')
   def test_api(mock_get):
       mock_get.return_value.status_code = 200
   ```

---

## 추가 리소스

- [TDD_GUIDE.md](./TDD_GUIDE.md) - TDD 상세 가이드
- [Pytest 문서](https://docs.pytest.org/)
- [Playwright 문서](https://playwright.dev/python/)
- [Factory Boy 문서](https://factoryboy.readthedocs.io/)

---

## 빠른 참조

```bash
# 설치
make install && make install-playwright

# 개발
make test-watch          # TDD 모드
make run                 # 서버 실행

# 테스트
make test                # 전체
make test-unit           # 단위
make test-integration    # 통합
make test-e2e            # E2E
make test-cov            # 커버리지

# 품질
make format              # 포맷팅
make lint                # 린팅
make ci                  # 전체 CI 체크

# 유틸리티
make clean               # 정리
make help                # 도움말
```
