import datetime
from typing import Any, List, Optional

from models.user import User
from services.dao_protocols import UserDAOProtocol


class UserService:
    def __init__(self, user_dao: UserDAOProtocol) -> None:
        self._dao = user_dao

    def find_or_create(self, user_id: int) -> Optional[User]:
        return self._dao.find_or_create(user_id)

    def update_user(self, user_id: int, **fields: Any) -> None:
        self._dao.update(user_id, **fields)

    def get_leaderboard(self, limit: int = 10) -> List[User]:
        return self._dao.get_leaderboard(limit)

    def get_cooldown(self, last_time: Optional[datetime.datetime], seconds_needed: int) -> Optional[int]:
        if not last_time:
            return None

        if last_time.tzinfo is None:
            last_time = last_time.replace(tzinfo=datetime.timezone.utc)

        now = datetime.datetime.now(datetime.timezone.utc)
        diff = now - last_time
        if diff.total_seconds() < seconds_needed:
            return seconds_needed - int(diff.total_seconds())
        return None

    def now_utc(self) -> datetime.datetime:
        return datetime.datetime.now(datetime.timezone.utc)
