from datetime import datetime
from typing import Dict

from bitronit.utils import json_to_object


class DailyAssetBalance:
    amount: float
    amount_try: float
    amount_usd: float

class DailyBalance:
    assets: Dict[str, DailyAssetBalance]
    date: datetime

    @staticmethod
    def json_parse(json_data):
        result = json_to_object(json_data, DailyBalance())
        for k, v in result.assets.items():
            result.assets[k] = json_to_object(v, DailyAssetBalance())
        return result