# api_get_user.py

from fastapi import APIRouter, Depends
from httpx import AsyncClient, HTTPStatusError
from utils.json_utils import get_headers
from utils.auth import get_token_from_header

router = APIRouter()
USER_URL = "https://api.libreview.ru/user"

@router.get("/user")
async def get_user_info(token: str = Depends(get_token_from_header)):
    headers = get_headers(token)
    headers["Accept"] = "application/json, application/xml"

    async with AsyncClient(verify=False, headers=headers) as client:
        try:
            response = await client.get(USER_URL)
            response.raise_for_status()
            json_data = response.json()
            user = json_data.get("data", {}).get("user", {})

            # Извлекаем city из первого practice, если он есть
            practices = user.get("practices", {}) or {}
            city = ""
            if isinstance(practices, dict) and practices:
                first_practice = next(iter(practices.values()))
                city = first_practice.get("city", "") or ""
                hospital_name = first_practice.get("name", "") or ""
                hospital_phone = first_practice.get("phoneNumber") or ""

            return {
                "firstName": user.get("firstName", ""),
                "lastName":  user.get("lastName", ""),
                "dateOfBirth": user.get("dateOfBirth", ""),
                "email":     user.get("email", ""),
                "hospitalName": hospital_name,
                "hospitalPhone": hospital_phone,
                "country":   user.get("country", ""),
                "city":      city,
                "errors":    ""
            }

        except HTTPStatusError as e:
            return {
                "firstName": "",
                "lastName":  "",
                "dateOfBirth": "",
                "email":     "",
                "country":   "",
                "city":      "",
                "errors":    f"HTTP error: {e.response.status_code}"
            }
        except Exception as e:
            return {
                "firstName": "",
                "lastName":  "",
                "dateOfBirth": "",
                "email":     "",
                "country":   "",
                "city":      "",
                "errors":    str(e)
            }
