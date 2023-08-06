from uuid import UUID
from datetime import datetime


class Transaction:
    hash: int
    base_asset: str
    quote_asset: str
    order_uuid: UUID
    transaction_date: datetime
    matched_quantity: float
    matched_price: float
    order_type: str
    fee_amount: float
    buyer: bool

