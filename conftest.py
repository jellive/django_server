"""Pytest configuration file"""
import pytest
from rest_framework.test import APIClient


@pytest.fixture
def api_client():
    """API 클라이언트 fixture"""
    return APIClient()


@pytest.fixture
def client():
    """Django test client fixture"""
    return APIClient()
