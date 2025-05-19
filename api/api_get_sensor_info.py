# api_get_sensor_info.py

from fastapi import APIRouter, Depends
from httpx import HTTPStatusError, AsyncClient
from utils.json_utils import extract_sensor_info, get_headers
from utils.auth import get_token_from_header

router = APIRouter()
SENSOR_URL = "https://api.libreview.ru/llu/connections"

@router.get("/sensor")
async def get_sensor_info(token: str = Depends(get_token_from_header)):
    headers = get_headers(token)

    async with AsyncClient(verify=False, headers=headers) as client:
        try:
            response = await client.get(SENSOR_URL)
            response.raise_for_status()
            return extract_sensor_info(response.json())
        except HTTPStatusError as e:
            return {"error": f"HTTP error: {e.response.status_code}", "details": e.response.text}
        except Exception as e:
            return {"error": str(e)}
