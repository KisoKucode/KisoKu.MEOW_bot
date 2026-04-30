from __future__ import annotations
from dataclasses import dataclass
from typing import Any, Dict, Optional


@dataclass
class Panel:
    id: int
    guild_id: int
    channel_id: int
    message_id: int

    @classmethod
    def from_record(cls, record: Dict[str, Any]) -> Optional["Panel"]:
        if not record:
            return None
        return cls(
            id=record.get("id", 1),
            guild_id=record.get("guild_id"),
            channel_id=record.get("channel_id"),
            message_id=record.get("message_id"),
        )
