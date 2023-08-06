from uuid import UUID
from datetime import datetime


class CryptoExternalTransaction:
    id: int
    type: str
    transaction_hash: str
    transaction_uuid: UUID
    address: str
    asset: str
    amount: int
    fee: float
    status: str
    confirmed_block_count: int
    status_update_date: datetime
    complete_date: datetime
    network: str
