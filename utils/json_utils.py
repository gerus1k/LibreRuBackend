# json_utils.py

from datetime import datetime, timedelta
from typing import Any

def get_headers(token: str | None = None) -> dict:
    headers = {
        "Accept": "application/json",
        "product": "llu.android",
        "version": "4.7"
    }
    if token:
        headers["Authorization"] = f"Bearer {token}"
    return headers


def extract_token(data: dict) -> str | None:
    try:
        return data["data"]["authTicket"]["token"]
    except (KeyError, TypeError):
        return None

def extract_glucose(data: dict) -> dict[str, Any] | None:
    try:
        glucose_item = data.get("data", [{}])[0].get("glucoseItem", {})
        value = glucose_item.get("Value")
        trend = glucose_item.get("TrendArrow")
        timestamp_str = glucose_item.get("Timestamp")

        if not timestamp_str:
            return {"error": "No timestamp in data."}

        timestamp = datetime.strptime(timestamp_str, "%m/%d/%Y %I:%M:%S %p")

        now = datetime.now()
        max_age = timedelta(minutes=5)

        if now - timestamp > max_age:
            return {
                "value": value,
                "trend": trend,
                "timestamp": timestamp_str,
                "errors": "staleData"
            }

        return {
            "value": value,
            "trend": trend,
            "timestamp": timestamp_str,
            "errors": ""
        }

    except (KeyError, TypeError, ValueError) as e:
        return {"error": f"Failed to extract glucose data: {str(e)}"}

def extract_patient_id(data: dict) -> str | None :
    try:
        return data["data"]["user"]["id"]
    except (KeyError, TypeError):
        return  None

def extract_graph(data: dict) -> list | None:
    try:
        graph_items = data["data"]["graphData"]
        return [
            {
                "timestamp": item.get("Timestamp"),
                "value": item.get("Value")
            }
            for item in graph_items
        ]
    except(KeyError, TypeError):
        return None

def extract_sensor_info(data: dict) -> dict[str, Any] | None:
    try:
        return {
            "activationTimestamp": data.get("data", [{}])[0].get("sensor", {}).get("a"),
            "expiresTimestamp": data.get("data", [{}])[0].get("sensor", {}).get("a") + 1209600,
            "serialNumber": "3" + data.get("data", [{}])[0].get("sensor", {}).get("sn"),
            "supportPhone": "88001008807"
        }
    except (KeyError, TypeError):
        return None