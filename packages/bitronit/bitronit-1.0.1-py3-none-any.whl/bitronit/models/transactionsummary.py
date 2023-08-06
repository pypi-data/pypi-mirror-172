from datetime import datetime
from dateutil import parser

class TransactionSummary:

    base_asset: str
    quote_asset: str
    transaction_date: datetime
    matched_quantity: float
    matched_price: float
    buyer_taker: bool