from __future__ import annotations
from dataclasses import dataclass
import datetime
from typing import Any, Dict, Optional


@dataclass
class User:
    user_id: int
    balance: int = 200
    bank: int = 0
    xp: int = 0
    level: int = 1
    last_daily: Optional[datetime.datetime] = None
    last_work: Optional[datetime.datetime] = None
    last_crime: Optional[datetime.datetime] = None

    @classmethod
    def from_record(cls, record: Dict[str, Any]) -> "User":
        return cls(
            user_id=record["user_id"],
            balance=record.get("balance", 200) or 0,
            bank=record.get("bank", 0) or 0,
            xp=record.get("xp", 0) or 0,
            level=record.get("level", 1) or 1,
            last_daily=record.get("last_daily"),
            last_work=record.get("last_work"),
            last_crime=record.get("last_crime"),
        )
