# main.py

from datetime import datetime

from api import api_get_glucose, api_login, api_get_user, api_get_sensor_info, api_get_graph

from fastapi import FastAPI, Depends
from api.api_get_glucose import router as glucose_router
from api.api_get_sensor_info import router as sensor_router
from api.api_get_graph import router as graph_router
from api.api_login import router as login_router
from api.api_get_user import router as user_router
from api.utils.auth import get_token_from_header

app = FastAPI()

app.include_router(login_router)
app.include_router(glucose_router)
app.include_router(sensor_router)
app.include_router(graph_router)
app.include_router(user_router)


@app.get("/glucose")
def get_glucose():
    return {
        "glucose": 110,
        "trend": "↗️",
        "timestamp": datetime.now().isoformat()
    }

@app.post("/login")
async def login_into_libre_account():
    result = await api_login.login()
    return result

@app.get("/getGlucose")
async def get_last_glucose_reading():
    return await api_get_glucose.get_glucose()

@app.get("/graph")
async def get_glucose_data_via_graph():
    return await api_get_graph.get_graph_data()

@app.get("/sensor")
async def get_current_sensor_info():
    return await api_get_sensor_info.get_sensor_info()

@app.get("/user")
async def get_user_info(token: str = Depends(get_token_from_header)):
    return await api_get_user.get_user_info(token)