from typing import Any, Dict

from models.user import User
from services.results import ServiceResult
from services.service_protocols import UserServiceProtocol


class LevelService:
    def __init__(self, user_service: UserServiceProtocol) -> None:
        self._user_service = user_service

    def _xp_for_level(self, level: int) -> int:
        return level * 100

    def add_experience(self, user_id: int, xp_amount: int) -> ServiceResult[Dict[str, Any]]:
        user = self._user_service.find_or_create(user_id)
        if not user:
            return ServiceResult.fail('No se pudo obtener el usuario.')

        current_xp = user.xp
        current_level = user.level

        new_xp = current_xp + xp_amount
        xp_needed = self._xp_for_level(current_level)
        leveled_up = False

        if new_xp >= xp_needed:
            new_xp -= xp_needed
            current_level += 1
            leveled_up = True
            self._user_service.update_user(user_id, xp=new_xp, level=current_level)
        else:
            self._user_service.update_user(user_id, xp=new_xp)

        return ServiceResult.ok({
            'level': current_level,
            'xp': new_xp,
            'xp_needed': self._xp_for_level(current_level),
            'leveled_up': leveled_up,
            'previous_level': current_level - 1 if leveled_up else current_level
        })

    def get_user_level_info(self, user_id: int) -> ServiceResult[Dict[str, Any]]:
        user = self._user_service.find_or_create(user_id)
        if not user:
            return ServiceResult.ok({'level': 1, 'xp': 0, 'xp_needed': self._xp_for_level(1)})

        return ServiceResult.ok({
            'level': user.level,
            'xp': user.xp,
            'xp_needed': self._xp_for_level(user.level)
        })
