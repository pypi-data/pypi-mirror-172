from uuid import UUID
from datetime import datetime


class FiatExternalTransaction:
    id: int
    type: str
    transaction_uuid: UUID
    asset: str
    amount: float
    fee: float
    status: str
    status_update_date: datetime
    complete_date: datetime
    sender_iban: str
    sender_bank_name: str
    receiver_iban: str
    receiver_bank_name: str
