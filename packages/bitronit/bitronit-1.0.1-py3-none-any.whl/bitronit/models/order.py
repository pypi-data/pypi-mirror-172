from uuid import UUID
from datetime import datetime


class Order:
    id: int
    price: float
    order_type: str
    operation_direction: str
    quantity: float
    order_status: str
    match_status: str
    executed_quantity: float
    average_match_price: float
    uuid: UUID
    base_asset: str
    quote_asset: str
    order_time: datetime
    stop_price: float

