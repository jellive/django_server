import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from jellserver.models import Post


class PostAPITest(APITestCase):
    """Post API 테스트"""

    def setUp(self):
        """테스트 데이터 설정"""
        self.client = APIClient()
        self.post1 = Post.objects.create(
            title='첫 번째 게시물',
            context='첫 번째 내용',
            div='notice',
            writer='작성자1',
        )
        self.post2 = Post.objects.create(
            title='두 번째 게시물',
            context='두 번째 내용',
            div='free',
            writer='작성자2',
        )

    def test_get_post_list(self):
        """게시물 목록 조회 테스트"""
        url = reverse('post-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 2)

    def test_get_post_detail(self):
        """게시물 상세 조회 테스트"""
        url = reverse('post-detail', args=[self.post1.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], '첫 번째 게시물')

    def test_create_post(self):
        """게시물 생성 테스트"""
        url = reverse('post-list')
        data = {
            'title': '새 게시물',
            'context': '새 내용',
            'div': 'qna',
            'writer': '새 작성자',
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Post.objects.count(), 3)

    def test_update_post(self):
        """게시물 수정 테스트"""
        url = reverse('post-detail', args=[self.post1.id])
        data = {
            'title': '수정된 제목',
            'context': '수정된 내용',
            'div': 'notice',
            'writer': '작성자1',
        }
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.post1.refresh_from_db()
        self.assertEqual(self.post1.title, '수정된 제목')

    def test_filter_by_div(self):
        """구분별 필터링 테스트"""
        url = reverse('post-list')
        response = self.client.get(url, {'div': 'notice'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)

    def test_search_posts(self):
        """게시물 검색 테스트"""
        url = reverse('post-list')
        response = self.client.get(url, {'search': '첫 번째'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)

    def test_soft_delete(self):
        """소프트 삭제 테스트"""
        url = reverse('post-soft-delete', args=[self.post1.id])
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.post1.refresh_from_db()
        self.assertTrue(self.post1.deleted)


@pytest.mark.django_db
class TestPostAPIPytest:
    """Pytest를 사용한 Post API 테스트"""

    def test_post_list_api(self, client):
        """게시물 목록 API 테스트 (pytest)"""
        Post.objects.create(
            title='Pytest 게시물',
            context='Pytest 내용',
            div='test',
            writer='pytest',
        )
        url = reverse('post-list')
        response = client.get(url)
        assert response.status_code == 200
        assert len(response.data['results']) >= 1
