.PHONY: help install migrate run test lint format clean shell

help:
	@echo "Django Server Makefile Commands:"
	@echo "  make install      - Install dependencies"
	@echo "  make migrate      - Run database migrations"
	@echo "  make migrations   - Create new migrations"
	@echo "  make run          - Run development server"
	@echo "  make test         - Run tests"
	@echo "  make test-cov     - Run tests with coverage"
	@echo "  make lint         - Run all linters"
	@echo "  make format       - Format code with black and isort"
	@echo "  make shell        - Open Django shell"
	@echo "  make shell-plus   - Open enhanced Django shell"
	@echo "  make superuser    - Create superuser"
	@echo "  make clean        - Clean up cache and temp files"
	@echo "  make urls         - Show all URLs"

install:
	pip install -r requirements.txt

migrate:
	python manage.py migrate

migrations:
	python manage.py makemigrations

run:
	python manage.py runserver

test:
	pytest

test-cov:
	pytest --cov=. --cov-report=html --cov-report=term-missing

test-unit:
	pytest jellserver/tests/

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

dev: install migrate
	@echo "Development environment ready!"

ci: format lint test
	@echo "CI checks passed!"
