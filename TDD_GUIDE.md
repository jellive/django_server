# TDD (Test-Driven Development) 가이드

## 목차
1. [TDD란?](#tdd란)
2. [프로젝트 테스트 구조](#프로젝트-테스트-구조)
3. [TDD 워크플로우](#tdd-워크플로우)
4. [테스트 작성 가이드](#테스트-작성-가이드)
5. [테스트 실행](#테스트-실행)
6. [예제](#예제)

---

## TDD란?

Test-Driven Development(TDD)는 테스트를 먼저 작성하고, 그 테스트를 통과하는 코드를 작성하는 개발 방법론입니다.

### TDD의 3단계 사이클 (Red-Green-Refactor)

```
1. 🔴 Red: 실패하는 테스트 작성
2. 🟢 Green: 테스트를 통과하는 최소한의 코드 작성
3. 🔵 Refactor: 코드 개선 및 리팩토링
```

---

## 프로젝트 테스트 구조

```
django_server/
├── jellserver/
│   └── tests/           # 단위 테스트
│       ├── __init__.py
│       ├── factories.py # Test data factories
│       ├── test_models.py
│       ├── test_api.py
│       └── test_serializers.py
├── tests/               # 통합 및 E2E 테스트
│   ├── integration/     # 통합 테스트
│   │   └── test_post_integration.py
│   └── e2e/            # End-to-end 테스트
│       ├── test_api_e2e.py
│       └── test_browser_e2e.py
└── conftest.py         # Pytest 설정
```

### 테스트 유형

1. **단위 테스트 (Unit Tests)**
   - 위치: `jellserver/tests/`
   - 목적: 개별 함수, 메서드, 클래스 테스트
   - 빠르고 독립적

2. **통합 테스트 (Integration Tests)**
   - 위치: `tests/integration/`
   - 목적: 여러 컴포넌트 간 상호작용 테스트
   - 데이터베이스 포함

3. **E2E 테스트 (End-to-End Tests)**
   - 위치: `tests/e2e/`
   - 목적: 전체 시스템 워크플로우 테스트
   - 실제 브라우저/HTTP 요청 사용

---

## TDD 워크플로우

### 1. 새 기능 개발 시 TDD 적용

#### Step 1: 실패하는 테스트 작성 (Red)

```python
# jellserver/tests/test_models.py
import pytest
from jellserver.models import Post

@pytest.mark.django_db
def test_post_has_view_count():
    """게시물에 조회수 필드가 있어야 한다 (아직 구현 안됨)"""
    post = Post.objects.create(
        title='테스트',
        context='내용',
        div='notice',
        writer='작성자'
    )

    # 이 테스트는 실패할 것 (view_count 필드가 없음)
    assert hasattr(post, 'view_count')
    assert post.view_count == 0
```

**실행:**
```bash
pytest jellserver/tests/test_models.py::test_post_has_view_count
```

**결과:** ❌ FAILED (view_count 필드가 없음)

#### Step 2: 테스트를 통과하는 최소 코드 작성 (Green)

```python
# jellserver/models.py
class Post(models.Model):
    title = models.CharField('제목', max_length=127)
    context = models.TextField('내용')
    # ... 기존 필드들 ...

    # 새로 추가
    view_count = models.IntegerField('조회수', default=0)
```

**마이그레이션:**
```bash
python manage.py makemigrations
python manage.py migrate
```

**다시 실행:**
```bash
pytest jellserver/tests/test_models.py::test_post_has_view_count
```

**결과:** ✅ PASSED

#### Step 3: 리팩토링 (Refactor)

코드 개선, 중복 제거, 성능 최적화 등을 수행합니다.

---

## 테스트 작성 가이드

### Factory 사용하기

테스트 데이터 생성에는 Factory Boy를 사용합니다.

```python
# jellserver/tests/factories.py에 이미 정의됨
from jellserver.tests.factories import PostFactory

# 사용 예제
def test_something():
    post = PostFactory()  # 기본 값으로 게시물 생성
    notice = PostFactory(div='notice')  # 특정 값 지정
    posts = PostFactory.create_batch(10)  # 10개 생성
```

### Pytest Fixtures 활용

```python
import pytest

@pytest.fixture
def sample_post():
    """재사용 가능한 테스트 데이터"""
    return PostFactory()

def test_with_fixture(sample_post):
    assert sample_post.id is not None
```

### AAA 패턴 (Arrange-Act-Assert)

```python
def test_post_soft_delete():
    # Arrange (준비)
    post = PostFactory(deleted=False)

    # Act (실행)
    post.deleted = True
    post.save()

    # Assert (검증)
    assert post.deleted is True
```

---

## 테스트 실행

### 1. 전체 테스트 실행

```bash
make test
# 또는
pytest
```

### 2. 특정 파일만 실행

```bash
pytest jellserver/tests/test_models.py
```

### 3. 특정 테스트만 실행

```bash
pytest jellserver/tests/test_models.py::test_post_creation
```

### 4. 키워드로 필터링

```bash
pytest -k "post"  # 이름에 'post'가 포함된 테스트만
```

### 5. TDD 모드 (자동 재실행)

```bash
# 파일 변경 시 자동으로 테스트 재실행
ptw  # pytest-watch
# 또는
pytest-watch
```

### 6. 커버리지 포함

```bash
make test-cov
# 또는
pytest --cov=. --cov-report=html
open htmlcov/index.html  # 커버리지 리포트 확인
```

### 7. 병렬 실행 (빠른 테스트)

```bash
pytest -n auto  # CPU 코어 수만큼 병렬 실행
```

### 8. E2E 테스트만 실행

```bash
pytest tests/e2e/
```

### 9. 통합 테스트만 실행

```bash
pytest tests/integration/
```

---

## 예제

### 예제 1: 새 모델 필드 추가 (TDD)

**요구사항:** Post 모델에 '좋아요 수' 필드 추가

#### 1단계: 테스트 작성

```python
# jellserver/tests/test_models.py
@pytest.mark.django_db
def test_post_likes_count():
    post = PostFactory()
    assert post.likes_count == 0

    post.likes_count = 5
    post.save()

    post.refresh_from_db()
    assert post.likes_count == 5
```

#### 2단계: 실행 (실패 확인)

```bash
pytest jellserver/tests/test_models.py::test_post_likes_count
# ❌ AttributeError: 'Post' object has no attribute 'likes_count'
```

#### 3단계: 구현

```python
# jellserver/models.py
class Post(models.Model):
    # ... 기존 필드 ...
    likes_count = models.IntegerField('좋아요 수', default=0)
```

#### 4단계: 마이그레이션 & 재실행

```bash
python manage.py makemigrations
python manage.py migrate
pytest jellserver/tests/test_models.py::test_post_likes_count
# ✅ PASSED
```

---

### 예제 2: API 엔드포인트 추가 (TDD)

**요구사항:** 게시물 좋아요 증가 API

#### 1단계: API 테스트 작성

```python
# jellserver/tests/test_api.py
@pytest.mark.django_db
def test_like_post_api():
    post = PostFactory(likes_count=0)
    client = APIClient()

    url = reverse('post-like', args=[post.id])
    response = client.post(url)

    assert response.status_code == 200
    assert response.data['likes_count'] == 1

    post.refresh_from_db()
    assert post.likes_count == 1
```

#### 2단계: 실행 (실패 확인)

```bash
pytest jellserver/tests/test_api.py::test_like_post_api
# ❌ NoReverseMatch: Reverse for 'post-like' not found
```

#### 3단계: ViewSet에 액션 추가

```python
# jellserver/views.py
class PostViewSet(viewsets.ModelViewSet):
    # ... 기존 코드 ...

    @action(detail=True, methods=['post'])
    def like(self, request, pk=None):
        """게시물 좋아요"""
        post = self.get_object()
        post.likes_count += 1
        post.save()
        return Response({'likes_count': post.likes_count})
```

#### 4단계: 재실행

```bash
pytest jellserver/tests/test_api.py::test_like_post_api
# ✅ PASSED
```

---

### 예제 3: E2E 테스트 (전체 워크플로우)

```python
# tests/e2e/test_api_e2e.py
@pytest.mark.django_db
def test_complete_post_workflow_e2e(live_server):
    """게시물 생성 → 조회 → 좋아요 → 삭제 전체 워크플로우"""
    base_url = live_server.url

    with httpx.Client() as client:
        # 1. 게시물 생성
        create_response = client.post(
            f"{base_url}/api/post/",
            json={'title': 'E2E 테스트', 'context': '내용', 'div': 'notice', 'writer': '작성자'}
        )
        assert create_response.status_code == 201
        post_id = create_response.json()['id']

        # 2. 조회
        get_response = client.get(f"{base_url}/api/post/{post_id}/")
        assert get_response.status_code == 200

        # 3. 좋아요
        like_response = client.post(f"{base_url}/api/post/{post_id}/like/")
        assert like_response.status_code == 200
        assert like_response.json()['likes_count'] == 1

        # 4. 소프트 삭제
        delete_response = client.post(f"{base_url}/api/post/{post_id}/soft_delete/")
        assert delete_response.status_code == 200
```

---

## 모범 사례

### ✅ DO

1. **테스트를 먼저 작성하라**
   ```python
   # ✅ Good: 테스트 먼저
   def test_new_feature():
       # 구현되지 않은 기능 테스트
       pass

   # 그 다음 구현
   ```

2. **하나의 테스트는 하나의 것만 테스트**
   ```python
   # ✅ Good
   def test_post_creation():
       post = PostFactory()
       assert post.id is not None

   def test_post_has_title():
       post = PostFactory()
       assert post.title
   ```

3. **Factory 사용**
   ```python
   # ✅ Good
   post = PostFactory()

   # ❌ Bad
   post = Post.objects.create(
       title='test', context='test', div='notice', writer='test'
   )
   ```

4. **의미 있는 테스트 이름**
   ```python
   # ✅ Good
   def test_deleted_posts_are_excluded_from_list():
       pass

   # ❌ Bad
   def test_1():
       pass
   ```

### ❌ DON'T

1. **실제 외부 서비스 호출 금지**
   ```python
   # ❌ Bad: 실제 이메일 발송
   def test_send_email():
       send_email_to_user('real@email.com')  # 실제로 발송됨!

   # ✅ Good: Mock 사용
   @patch('myapp.send_email')
   def test_send_email(mock_send):
       send_email_to_user('test@email.com')
       mock_send.assert_called_once()
   ```

2. **테스트 간 의존성 금지**
   ```python
   # ❌ Bad
   def test_a():
       global post
       post = PostFactory()

   def test_b():
       assert post.title  # test_a에 의존
   ```

3. **너무 많은 것을 한 테스트에서 검증**
   ```python
   # ❌ Bad
   def test_everything():
       assert True
       assert 1 == 1
       assert "test" == "test"
       # ... 100줄 ...
   ```

---

## 유용한 명령어 요약

```bash
# TDD 개발 모드 (자동 재실행)
ptw

# 빠른 테스트 (병렬)
pytest -n auto

# 특정 테스트만
pytest -k "post_creation"

# 커버리지
make test-cov

# 실패한 테스트만 재실행
pytest --lf

# 상세 출력
pytest -v

# 출력 표시
pytest -s
```

---

## 추가 리소스

- [pytest 공식 문서](https://docs.pytest.org/)
- [Factory Boy 문서](https://factoryboy.readthedocs.io/)
- [Django Testing 가이드](https://docs.djangoproject.com/en/5.1/topics/testing/)
- [TDD by Example - Kent Beck](https://www.amazon.com/Test-Driven-Development-Kent-Beck/dp/0321146530)

---

## 팀 규칙

1. **모든 새 기능은 테스트와 함께 작성**
2. **커버리지 80% 이상 유지**
3. **PR 전에 `make test` 통과 필수**
4. **E2E 테스트는 중요 워크플로우만**
5. **테스트 실패 시 절대 커밋 금지**
