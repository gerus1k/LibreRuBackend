# api_get_glucose.py

from fastapi import APIRouter, Depends
from httpx import HTTPStatusError, AsyncClient
from api.utils.json_utils import extract_glucose, get_headers
from api.utils.auth import get_token_from_header

router = APIRouter()
GLUCOSE_URL = "https://api.libreview.ru/llu/connections"

@router.get("/getGlucose")
async def get_glucose(token: str = Depends(get_token_from_header)):
    headers = get_headers(token)

    async with AsyncClient(verify=False, headers=headers) as client:
        try:
            response = await client.get(GLUCOSE_URL)
            response.raise_for_status()
            return extract_glucose(response.json())
        except HTTPStatusError as e:
            return {"error": f"HTTP error: {e.response.status_code}", "details": e.response.text}
        except Exception as e:
            return {"error": str(e)}
