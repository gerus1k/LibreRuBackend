# auth.py

from fastapi import Header, HTTPException

async def get_token_from_header(authorization: str = Header(...)):
    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Неверный формат токена")
    return authorization.split(" ")[1]
