from datetime import datetime
from typing import Dict


class Orderbook:
    timestamp: datetime
    version: int
    sell: Dict[str, float]
    buy: Dict[str, float]
