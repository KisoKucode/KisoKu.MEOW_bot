from typing import Dict

from services.results import ServiceResult
from services.service_protocols import HangmanServiceProtocol, UserServiceProtocol


class HangmanService(HangmanServiceProtocol):
    def __init__(self, user_service: UserServiceProtocol) -> None:
        self._user_service = user_service

    def reward_for_win(self, user_id: int, reward: int) -> ServiceResult[Dict[str, int]]:
        user = self._user_service.find_or_create(user_id)
        if not user:
            return ServiceResult.fail('No se pudo obtener el usuario.')

        new_balance = user.balance + reward
        self._user_service.update_user(user_id, balance=new_balance)
        return ServiceResult.ok({'balance': new_balance, 'reward': reward})
