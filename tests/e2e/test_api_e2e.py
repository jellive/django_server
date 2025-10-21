"""
E2E API Tests using httpx

These tests make actual HTTP requests to the running server
to test the entire stack from HTTP request to database.
"""
import pytest
import httpx
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken

from jellserver.tests.factories import PostFactory


@pytest.mark.django_db
class TestPostAPIE2E:
    """Post API E2E 테스트"""

    @pytest.fixture(autouse=True)
    def setup(self, live_server):
        """테스트 설정"""
        self.base_url = live_server.url
        self.api_url = f"{self.base_url}/api"

        # 테스트 사용자 생성
        self.user = User.objects.create_user(
            username='testuser', password='testpass123', email='test@example.com'
        )

        # JWT 토큰 생성
        refresh = RefreshToken.for_user(self.user)
        self.access_token = str(refresh.access_token)
        self.headers = {'Authorization': f'Bearer {self.access_token}'}

    def test_create_post_e2e(self):
        """게시물 생성 E2E 테스트"""
        with httpx.Client() as client:
            data = {
                'title': 'E2E 테스트 제목',
                'context': 'E2E 테스트 내용',
                'div': 'notice',
                'writer': 'E2E Tester',
            }

            response = client.post(f"{self.api_url}/post/", json=data, headers=self.headers)

            assert response.status_code == 201
            json_data = response.json()
            assert json_data['title'] == 'E2E 테스트 제목'
            assert json_data['context'] == 'E2E 테스트 내용'
            assert 'id' in json_data

    def test_list_posts_e2e(self):
        """게시물 목록 조회 E2E 테스트"""
        # 테스트 데이터 생성
        PostFactory.create_batch(5)

        with httpx.Client() as client:
            response = client.get(f"{self.api_url}/post/")

            assert response.status_code == 200
            json_data = response.json()
            assert 'results' in json_data
            assert len(json_data['results']) == 5

    def test_filter_posts_by_div_e2e(self):
        """게시물 필터링 E2E 테스트"""
        PostFactory.create_batch(3, div='notice')
        PostFactory.create_batch(2, div='free')

        with httpx.Client() as client:
            response = client.get(f"{self.api_url}/post/", params={'div': 'notice'})

            assert response.status_code == 200
            json_data = response.json()
            assert len(json_data['results']) == 3

    def test_search_posts_e2e(self):
        """게시물 검색 E2E 테스트"""
        PostFactory(title='찾을 수 있는 제목')
        PostFactory(title='다른 제목')

        with httpx.Client() as client:
            response = client.get(f"{self.api_url}/post/", params={'search': '찾을 수 있는'})

            assert response.status_code == 200
            json_data = response.json()
            assert len(json_data['results']) == 1
            assert '찾을 수 있는' in json_data['results'][0]['title']

    def test_update_post_e2e(self):
        """게시물 수정 E2E 테스트"""
        post = PostFactory()

        with httpx.Client() as client:
            data = {
                'title': '수정된 제목',
                'context': post.context,
                'div': post.div,
                'writer': post.writer,
            }

            response = client.put(
                f"{self.api_url}/post/{post.id}/", json=data, headers=self.headers
            )

            assert response.status_code == 200
            json_data = response.json()
            assert json_data['title'] == '수정된 제목'

    def test_soft_delete_post_e2e(self):
        """게시물 소프트 삭제 E2E 테스트"""
        post = PostFactory()

        with httpx.Client() as client:
            response = client.post(
                f"{self.api_url}/post/{post.id}/soft_delete/", headers=self.headers
            )

            assert response.status_code == 200
            assert response.json()['status'] == 'deleted'

            # 삭제된 게시물이 목록에 나타나지 않는지 확인
            list_response = client.get(f"{self.api_url}/post/")
            json_data = list_response.json()
            post_ids = [p['id'] for p in json_data['results']]
            assert post.id not in post_ids

    def test_pagination_e2e(self):
        """페이지네이션 E2E 테스트"""
        PostFactory.create_batch(25)

        with httpx.Client() as client:
            response = client.get(f"{self.api_url}/post/", params={'page': 1})

            assert response.status_code == 200
            json_data = response.json()
            assert 'next' in json_data
            assert 'previous' in json_data
            assert len(json_data['results']) == 10  # Default page size


@pytest.mark.django_db
class TestAuthE2E:
    """인증 E2E 테스트"""

    @pytest.fixture(autouse=True)
    def setup(self, live_server):
        self.base_url = live_server.url
        self.api_url = f"{self.base_url}/api"

    def test_jwt_token_obtain_e2e(self):
        """JWT 토큰 발급 E2E 테스트"""
        user = User.objects.create_user(username='testuser', password='testpass123')

        with httpx.Client() as client:
            response = client.post(
                f"{self.api_url}/token/", json={'username': 'testuser', 'password': 'testpass123'}
            )

            assert response.status_code == 200
            json_data = response.json()
            assert 'access' in json_data
            assert 'refresh' in json_data

    def test_jwt_token_refresh_e2e(self):
        """JWT 토큰 갱신 E2E 테스트"""
        user = User.objects.create_user(username='testuser', password='testpass123')
        refresh = RefreshToken.for_user(user)

        with httpx.Client() as client:
            response = client.post(f"{self.api_url}/token/refresh/", json={'refresh': str(refresh)})

            assert response.status_code == 200
            json_data = response.json()
            assert 'access' in json_data
