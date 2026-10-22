import requests
import pytest

BASE_URL = "http://127.0.0.1:8000"

@pytest.mark.parametrize("amount, expected_status", [
    (500.0, "正常"),
    (2500.0, "预警"),
    (4000.0, "超支拦截")
])
def test_budget_warning(amount, expected_status):
    """测试预算预警的边界值"""
    payload = {"amount": amount, "budget": 3000}
    res = requests.post(f"{BASE_URL}/expense", json=payload)
    assert res.status_code == 200
    assert res.json()["status"] == expected_status