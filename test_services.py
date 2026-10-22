import pytest
from services import get_amap_route


def test_amap_route_mock_success(mocker):
    """模拟地图API正常返回（隔离网络）"""
    # 拦截 requests.get
    mock_get = mocker.patch("requests.get")
    # 伪造高德返回的数据
    mock_get.return_value.json.return_value = {
        "status": "1",
        "route": {"paths": [{"distance": "15000"}]}
    }

    result = get_amap_route(116.0, 39.0, 117.0, 40.0)

    assert result["route"]["paths"][0]["distance"] == "15000"
    mock_get.assert_called_once()


def test_amap_route_mock_failure(mocker):
    """模拟地图API宕机或超时（验证容错）"""
    mock_get = mocker.patch("requests.get")
    # 强行让请求抛出超时异常
    mock_get.side_effect = Exception("Timeout")

    with pytest.raises(Exception) as exc_info:
        get_amap_route(116.0, 39.0, 117.0, 40.0)
    assert str(exc_info.value) == "Timeout"