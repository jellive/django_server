"""
E2E Browser Tests using Playwright

These tests open a real browser and interact with the application
to test user workflows from the browser perspective.
"""
import pytest
from playwright.sync_api import Page, expect
from django.contrib.auth.models import User

from jellserver.tests.factories import PostFactory


@pytest.mark.django_db
@pytest.mark.playwright
class TestAdminE2E:
    """Admin 페이지 E2E 테스트"""

    @pytest.fixture(autouse=True)
    def setup(self, live_server):
        """테스트 설정"""
        self.base_url = live_server.url

        # Superuser 생성
        self.admin_user = User.objects.create_superuser(
            username='admin', password='admin123', email='admin@example.com'
        )

        # 테스트 데이터 생성
        PostFactory.create_batch(3)

    def test_admin_login(self, page: Page):
        """Admin 로그인 테스트"""
        page.goto(f"{self.base_url}/admin/")

        # 로그인
        page.fill('input[name="username"]', 'admin')
        page.fill('input[name="password"]', 'admin123')
        page.click('input[type="submit"]')

        # 로그인 성공 확인
        expect(page.locator('body')).to_contain_text('Site administration')

    def test_admin_post_list(self, page: Page):
        """Admin 게시물 목록 테스트"""
        # 로그인
        page.goto(f"{self.base_url}/admin/")
        page.fill('input[name="username"]', 'admin')
        page.fill('input[name="password"]', 'admin123')
        page.click('input[type="submit"]')

        # 게시물 페이지로 이동
        page.click('a[href="/admin/jellserver/post/"]')

        # 게시물 목록 확인
        expect(page.locator('#result_list')).to_be_visible()

    def test_admin_create_post(self, page: Page):
        """Admin에서 게시물 생성 테스트"""
        # 로그인
        page.goto(f"{self.base_url}/admin/")
        page.fill('input[name="username"]', 'admin')
        page.fill('input[name="password"]', 'admin123')
        page.click('input[type="submit"]')

        # 게시물 추가 페이지로 이동
        page.goto(f"{self.base_url}/admin/jellserver/post/add/")

        # 폼 작성
        page.fill('input[name="title"]', '브라우저 E2E 테스트 제목')
        page.fill('textarea[name="context"]', '브라우저 E2E 테스트 내용')
        page.fill('input[name="writer"]', 'E2E Admin')
        page.select_option('select[name="div"]', 'notice')

        # 저장
        page.click('input[name="_save"]')

        # 성공 메시지 확인
        expect(page.locator('.success')).to_contain_text('successfully')


@pytest.mark.django_db
@pytest.mark.playwright
class TestAPIDocsE2E:
    """API 문서 페이지 E2E 테스트"""

    @pytest.fixture(autouse=True)
    def setup(self, live_server):
        self.base_url = live_server.url

    def test_swagger_ui_loads(self, page: Page):
        """Swagger UI 로드 테스트"""
        page.goto(f"{self.base_url}/api/docs/")

        # Swagger UI 로드 확인
        expect(page.locator('.swagger-ui')).to_be_visible()
        expect(page).to_have_title('Jell Server API')

    def test_redoc_loads(self, page: Page):
        """ReDoc 로드 테스트"""
        page.goto(f"{self.base_url}/api/redoc/")

        # ReDoc 로드 확인
        expect(page.locator('[role="navigation"]')).to_be_visible()


@pytest.mark.django_db
@pytest.mark.playwright
class TestHealthCheckE2E:
    """헬스 체크 E2E 테스트"""

    @pytest.fixture(autouse=True)
    def setup(self, live_server):
        self.base_url = live_server.url

    def test_health_check(self, page: Page):
        """헬스 체크 엔드포인트 테스트"""
        response = page.goto(f"{self.base_url}/health/")

        assert response.status == 200
