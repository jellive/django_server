.PHONY: help install migrate run test lint format clean shell

help:
	@echo "Django Server Makefile Commands:"
	@echo ""
	@echo "Setup:"
	@echo "  make install         - Install dependencies"
	@echo "  make install-playwright - Install Playwright browsers"
	@echo "  make dev             - Setup development environment"
	@echo ""
	@echo "Database:"
	@echo "  make migrate         - Run database migrations"
	@echo "  make migrations      - Create new migrations"
	@echo ""
	@echo "Running:"
	@echo "  make run             - Run development server"
	@echo "  make shell           - Open Django shell"
	@echo "  make shell-plus      - Open enhanced Django shell"
	@echo ""
	@echo "Testing (TDD):"
	@echo "  make test            - Run all tests"
	@echo "  make test-unit       - Run unit tests only"
	@echo "  make test-integration - Run integration tests only"
	@echo "  make test-e2e        - Run E2E tests only"
	@echo "  make test-cov        - Run tests with coverage report"
	@echo "  make test-watch      - TDD mode (auto-rerun on changes)"
	@echo "  make test-parallel   - Run tests in parallel (fast)"
	@echo ""
	@echo "Code Quality:"
	@echo "  make lint            - Run all linters"
	@echo "  make format          - Format code with black and isort"
	@echo "  make ci              - Run full CI checks"
	@echo ""
	@echo "Utilities:"
	@echo "  make superuser       - Create superuser"
	@echo "  make clean           - Clean up cache and temp files"
	@echo "  make urls            - Show all URLs"

install:
	pip install -r requirements.txt

install-playwright:
	playwright install --with-deps chromium

migrate:
	python manage.py migrate

migrations:
	python manage.py makemigrations

run:
	python manage.py runserver

# === Testing (TDD) ===

test:
	@echo "Running all tests..."
	pytest

test-unit:
	@echo "Running unit tests..."
	pytest jellserver/tests/ -v

test-integration:
	@echo "Running integration tests..."
	pytest tests/integration/ -v

test-e2e:
	@echo "Running E2E tests..."
	pytest tests/e2e/ -v

test-e2e-headed:
	@echo "Running E2E tests with visible browser..."
	pytest tests/e2e/ --headed

test-cov:
	@echo "Running tests with coverage..."
	pytest --cov=. --cov-report=html --cov-report=term-missing
	@echo "Coverage report generated at htmlcov/index.html"

test-watch:
	@echo "TDD mode: Tests will auto-run on file changes..."
	ptw --runner "pytest -x"

test-parallel:
	@echo "Running tests in parallel..."
	pytest -n auto

test-failed:
	@echo "Re-running failed tests..."
	pytest --lf -v

lint:
	@echo "Running flake8..."
	flake8
	@echo "Running pylint..."
	pylint jellserver/
	@echo "Running mypy..."
	mypy .

format:
	@echo "Running black..."
	black .
	@echo "Running isort..."
	isort .

shell:
	python manage.py shell

shell-plus:
	python manage.py shell_plus

superuser:
	python manage.py createsuperuser

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".mypy_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name "htmlcov" -exec rm -rf {} + 2>/dev/null || true
	rm -f .coverage

urls:
	python manage.py show_urls

check:
	python manage.py check

collectstatic:
	python manage.py collectstatic --no-input

dev: install install-playwright migrate
	@echo "Development environment ready!"
	@echo "Run 'make test-watch' to start TDD mode"

ci: format lint test-parallel
	@echo "CI checks passed!"

tdd: test-watch
