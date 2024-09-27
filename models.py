from pydantic import BaseModel

class OrderParams(BaseModel):
    symbol: str
    side: int  # 1: open long, 2: close short, 3: open short, 4: close long
    openType: int  # 1: isolated, 2: cross
    type: str  # 5: Market order
    vol: float  # Объём заказа
    leverage: int  # Кредитное плечо
    marketCeiling: bool = False
    priceProtect: str = "0"
    reduceOnly: bool = False

class TriggerOrderParams(BaseModel):
    symbol: str
    side: int
    orderType: int  # 5: Market order
    executeCycle: int  # 1: 24h, 2: 7d, 3: no limit
    openType: int
    trend: str  # 1: last price, 2: fair price, 3: index price
    vol: float
    leverage: int
    marketCeiling: bool = False
    priceProtect: str = "0"
    reduceOnly: bool = False
    triggerType: int  # 2: if price is below current price, 1: if price is above it for long
    triggerPrice: float

class TrailingOrderParams(BaseModel):
    symbol: str
    leverage: int
    side: int
    vol: float
    openType: int
    trend: str  # 1: last price, 2: fair price, 3: index price
    backType: str  # 1: Trail variance in %, 2: price difference in USDT
    positionMode: int
    backValue: float

class CancelOrderParams(BaseModel):
    orderIds: list[str]
