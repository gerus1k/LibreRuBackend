# api_login.py

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import httpx
from utils.json_utils import extract_token, extract_patient_id, get_headers

router = APIRouter()

AUTH_URL = "https://api.libreview.ru/llu/auth/login"

class LoginRequest(BaseModel):
    email: str
    password: str

@router.post("/login")
async def login(request: LoginRequest):
    payload = {
        "email": request.email,
        "password": request.password
    }

    headers = get_headers(token=None)  # токена ещё нет, только product/version/accept

    headers.pop("Authorization", None)

    async with httpx.AsyncClient(verify=False, headers=headers) as client:
        try:
            response = await client.post(AUTH_URL, json=payload)
            response.raise_for_status()
            data = response.json()

            if data.get("status") == 2 or "error" in data:
                raise HTTPException(status_code=401, detail="Неверный email или пароль")

            access_token = extract_token(data)
            patient_id = extract_patient_id(data)

            if not access_token or not patient_id:
                raise HTTPException(status_code=500, detail="Не получен токен или ID")

            return {
                "status": "success",
                "token": access_token,
                "patientId": patient_id
            }

        except httpx.RequestError:
            raise HTTPException(status_code=504, detail="Сервер Libre не отвечает")
        except httpx.HTTPStatusError as e:
            raise HTTPException(status_code=e.response.status_code, detail="Ошибка авторизации")
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
