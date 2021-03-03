from datetime import datetime

from pydantic import Field
from pydantic.main import BaseModel


class Symbol24PriceSchema(BaseModel):
    symbol: str
    price_change: float = Field(..., alias='priceChange')
    price_change_percent: float = Field(..., alias='priceChangePercent')
    weighted_avg_price: float = Field(..., alias='weightedAvgPrice')
    prev_close_price: float = Field(..., alias='prevClosePrice')
    last_price: float = Field(..., alias='lastPrice')
    last_qty: float = Field(..., alias='lastQty')
    bid_price: float = Field(..., alias='bidPrice')
    bid_qty: float = Field(..., alias='bidQty')
    ask_price: float = Field(..., alias='askPrice')
    ask_qty: float = Field(..., alias='askQty')
    open_price: float = Field(..., alias='openPrice')
    high_price: float = Field(..., alias='highPrice')
    low_price: float = Field(..., alias='lowPrice')
    volume: float
    quote_volume: float = Field(..., alias='quoteVolume')
    open_time: datetime = Field(..., alias='openTime')
    close_time: datetime = Field(..., alias='closeTime')
    first_id: int = Field(..., alias='firstId')
    last_id: int = Field(..., alias='lastId')
    count: int

