import requests


def get_amap_route(origin_lng, origin_lat, dest_lng, dest_lat):
    """调用高德地图API获取路线"""
    amap_key = "YOUR_AMAP_KEY"  # 如果没有真实的Key，随便写一个，反正我们测试时会Mock拦截
    url = f"https://restapi.amap.com/v3/direction/driving?origin={origin_lng},{origin_lat}&destination={dest_lng},{dest_lat}&key={amap_key}"

    # 真实发送请求
    response = requests.get(url, timeout=5)
    return response.json()