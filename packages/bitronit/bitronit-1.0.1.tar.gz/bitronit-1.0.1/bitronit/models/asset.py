from datetime import datetime

class Asset:
    id: int
    ticker: str
    full_name: str
    circulating_supply: float
    circulating_supply_update_date: datetime
    precision: int
    fiat: bool
