from fastapi import FastAPI, HTTPException
from models import OrderParams, TriggerOrderParams, TrailingOrderParams, CancelOrderParams
import time
import hashlib
import requests

app = FastAPI(
    title="Exchange API",  # Новый заголовок
    description="Все точки доступа к API биржи",  # Описание API
    version="1.0.0",  # Версия API
)

# Конфигурационные переменные
AUTHORIZATION_KEY = "WEB1e95f5d65acf925255b9bd02e849743uhfjnkwfffbe3667952fbd66c43a1dc09df"
BASE_URL = "https://futures.mexc.com/api/v1/private"

# Вспомогательная функция для генерации подписи
def generate_signature(params: dict, timestamp: int) -> str:
    param_string = str(params)
    hash_input = f"{timestamp}{param_string}{AUTHORIZATION_KEY}"
    return hashlib.md5(hash_input.encode()).hexdigest()

# Общий метод для отправки запросов к бирже
def send_request(url: str, params: dict) -> dict:
    timestamp = int(time.time() * 1000)
    signature = generate_signature(params, timestamp)

    headers = {
        "x-mxc-nonce": str(timestamp),
        "x-mxc-sign": signature,
        "authorization": AUTHORIZATION_KEY,
        "user-agent": "MEXC/7 CFNetwork/1474 Darwin/23.0.0",
        "content-type": "application/json",
        "origin": "https://futures.mexc.com",
        "referer": "https://futures.mexc.com/exchange",
    }

    response = requests.post(url, json=params, headers=headers)

    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail="Error from exchange API")

    return response.json()

# Эндпоинты FastAPI

@app.post("/order/create")
async def create_order(order_params: OrderParams):
    """Создание ордера"""
    url = f"{BASE_URL}/order/create"
    params = order_params.dict()
    return send_request(url, params)

@app.post("/order/trigger")
async def create_trigger_order(trigger_order_params: TriggerOrderParams):
    """Создание триггерного ордера"""
    url = f"{BASE_URL}/planorder/place"
    params = trigger_order_params.dict()
    return send_request(url, params)

@app.post("/order/trailing")
async def create_trailing_order(trailing_order_params: TrailingOrderParams):
    """Создание трейлинг-ордера"""
    url = f"{BASE_URL}/trackorder/place"
    params = trailing_order_params.dict()
    return send_request(url, params)

@app.post("/order/cancel")
async def cancel_order(cancel_order_params: CancelOrderParams):
    """Отмена ордера"""
    url = f"{BASE_URL}/order/cancel"
    params = {"orderIds": cancel_order_params.orderIds}
    return send_request(url, params)
