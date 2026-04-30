from typing import Dict

from services.results import ServiceResult
from services.service_protocols import ShopServiceProtocol, UserServiceProtocol


class ShopService(ShopServiceProtocol):
    def __init__(self, user_service: UserServiceProtocol) -> None:
        self._user_service = user_service

    def purchase_role(self, user_id: int, price: int) -> ServiceResult[Dict[str, int]]:
        user = self._user_service.find_or_create(user_id)
        if not user:
            return ServiceResult.fail('No se pudo obtener el usuario.')

        if user.balance < price:
            return ServiceResult.fail(f'No tienes suficientes monedas. Tu saldo actual es {user.balance}.')

        new_balance = user.balance - price
        self._user_service.update_user(user_id, balance=new_balance)
        return ServiceResult.ok({'balance': new_balance})
