from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
from services import get_amap_route

app = FastAPI(title="旅行手账 API")


class ExpenseReq(BaseModel):
    amount: float
    budget: float


class Coordinate(BaseModel):
    lat: float
    lng: float


@app.post("/expense")
def add_expense(req: ExpenseReq):
    """预算预警逻辑"""
    if req.amount > req.budget:
        return {"status": "超支拦截", "msg": "已超支"}
    elif req.amount >= req.budget * 0.8:
        return {"status": "预警", "msg": "预算已达80%"}
    return {"status": "正常", "msg": "记账成功"}


@app.post("/route/plan")
def plan_route(coords: List[Coordinate]):
    """路线规划接口"""
    if len(coords) < 2:
        return {"code": 400, "message": "至少需要2个点"}

    try:
        # 调用 services.py 里的底层方法
        data = get_amap_route(coords[0].lng, coords[0].lat, coords[-1].lng, coords[-1].lat)
        if data.get("status") == "1":
            return {"code": 200, "distance": data["route"]["paths"][0]["distance"]}
        return {"code": 500, "message": "高德API报错"}
    except Exception as e:
        # 容错降级：如果第三方API挂了，系统不能崩
        return {"code": 503, "message": "地图服务暂时不可用"}