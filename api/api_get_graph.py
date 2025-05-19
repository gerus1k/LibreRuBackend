# api_get_graph.py

from typing import List
from fastapi import APIRouter, Depends, Query
from httpx import HTTPStatusError, AsyncClient
from pydantic import BaseModel
from utils.json_utils import extract_graph, get_headers
from utils.auth import get_token_from_header

router = APIRouter()
GRAPH_URL_TEMPLATE = "https://api.libreview.ru/llu/connections/{patientId}/graph"


class GlucosePoint(BaseModel):
    timestamp: str
    value: float


class GraphResponse(BaseModel):
    data: List[GlucosePoint] | None
    errors: str


@router.get("/graph", response_model=GraphResponse)
async def get_graph_data(
    token: str = Depends(get_token_from_header),
    patient_id: str = Query(...)
):
    headers = get_headers(token)
    graph_url = GRAPH_URL_TEMPLATE.format(patientId=patient_id)

    try:
        async with AsyncClient(verify=False, headers=headers) as client:
            response = await client.get(graph_url)
            response.raise_for_status()
            raw = response.json()
    except HTTPStatusError as e:
        return GraphResponse(data=None, errors=f"HTTP error: {e.response.status_code}")
    except Exception as e:
        return GraphResponse(data=None, errors=str(e))

    extracted = extract_graph(raw)
    if extracted is None:
        return GraphResponse(data=None, errors="Failed to extract graph data")

    return GraphResponse(data=extracted, errors="")
