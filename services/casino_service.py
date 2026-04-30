import datetime
from typing import Any, Dict, List

from config import DAILY_AMOUNT
from models.user import User
from services.game_strategies import BlackjackStrategy, CoinFlipStrategy, SlotStrategy
from services.results import ServiceResult
from services.service_protocols import CasinoServiceProtocol, UserServiceProtocol


class CasinoService(CasinoServiceProtocol):
    def __init__(self, user_service: UserServiceProtocol) -> None:
        self._user_service = user_service
        self._slot_strategy = SlotStrategy()
        self._coin_flip_strategy = CoinFlipStrategy()
        self._blackjack_strategy = BlackjackStrategy()

    def validate_bet(self, user_id: int, bet: int) -> ServiceResult[dict[str, Any]]:
        if bet <= 0:
            return ServiceResult.fail('La apuesta debe ser mayor que cero.')

        user = self._user_service.find_or_create(user_id)
        if not user:
            return ServiceResult.fail('No se pudo obtener el usuario.')

        if user.balance < bet:
            return ServiceResult.fail(f'No tienes suficientes monedas. Tu saldo es de {user.balance}.')

        return ServiceResult.ok({'balance': user.balance})

    def collect_daily_reward(self, user_id: int, now: datetime.datetime | None = None) -> ServiceResult[dict[str, Any]]:
        if now is None:
            now = self._user_service.now_utc()

        user = self._user_service.find_or_create(user_id)
        if not user:
            return ServiceResult.fail('No se pudo obtener el usuario.')

        if user.last_daily:
            if user.last_daily.tzinfo is None:
                last_claim = user.last_daily.replace(tzinfo=datetime.timezone.utc)
            else:
                last_claim = user.last_daily

            elapsed = now - last_claim
            if elapsed.total_seconds() < 86400:
                remaining = int(86400 - elapsed.total_seconds())
                return ServiceResult.fail(f'Aún no puedes reclamar tu recompensa. Faltan {remaining // 3600} horas.')

        new_balance = user.balance + DAILY_AMOUNT
        self._user_service.update_user(user_id, balance=new_balance, last_daily=now)
        return ServiceResult.ok({'balance': new_balance, 'amount': DAILY_AMOUNT})

    def spin_slots(self, user_id: int, bet: int) -> ServiceResult[dict[str, Any]]:
        validation = self.validate_bet(user_id, bet)
        if not validation.success:
            return validation

        strategy_result = self._slot_strategy.execute(bet)
        if not strategy_result.success or not strategy_result.data:
            return ServiceResult.fail('Error al generar el resultado de la tragamonedas.')

        winnings = strategy_result.data['winnings']
        new_balance = validation.data['balance'] - bet + winnings
        self._user_service.update_user(user_id, balance=new_balance)

        return ServiceResult.ok({
            'result_text': strategy_result.data['result_text'],
            'winnings': winnings,
            'balance': new_balance,
            'bet': bet,
            'reels': strategy_result.data['reels'],
        })

    def coin_flip(self, user_id: int, bet: int, choice: str) -> ServiceResult[dict[str, Any]]:
        validation = self.validate_bet(user_id, bet)
        if not validation.success:
            return validation

        strategy_result = self._coin_flip_strategy.execute(choice, bet)
        if not strategy_result.success or not strategy_result.data:
            return ServiceResult.fail('Error al procesar el lanzamiento de la moneda.')

        balance = validation.data['balance']
        if strategy_result.data['won']:
            new_balance = balance + bet
        else:
            new_balance = balance - bet

        self._user_service.update_user(user_id, balance=new_balance)
        return ServiceResult.ok({
            'choice': strategy_result.data['choice'],
            'result': strategy_result.data['result'],
            'won': strategy_result.data['won'],
            'balance': new_balance,
            'bet': bet,
        })

    def settle_blackjack(
        self,
        user_id: int,
        player_value: int,
        dealer_value: int,
        bet: int,
        blackjack: bool = False,
    ) -> ServiceResult[dict[str, Any]]:
        user = self._user_service.find_or_create(user_id)
        if not user:
            return ServiceResult.fail('No se pudo obtener el usuario.')

        # Use the BlackjackStrategy to determine the outcome
        strategy_result = self._blackjack_strategy.execute(player_value, dealer_value, bet, blackjack)
        if not strategy_result.success or not strategy_result.data:
            return ServiceResult.fail('Error al determinar el resultado del Blackjack.')

        change = strategy_result.data['change']
        description = strategy_result.data['description']
        color = strategy_result.data['color']

        new_balance = user.balance + change
        self._user_service.update_user(user_id, balance=new_balance)
        return ServiceResult.ok({
            'balance': new_balance,
            'change': change,
            'description': description,
            'color': color,
        })

    def process_video_poker(self, user_id: int, bet: int, winnings: int) -> ServiceResult[dict[str, Any]]:
        user = self._user_service.find_or_create(user_id)
        if not user:
            return ServiceResult.fail('No se pudo obtener el usuario.')

        new_balance = user.balance - bet + winnings
        self._user_service.update_user(user_id, balance=new_balance)
        return ServiceResult.ok({'balance': new_balance, 'winnings': winnings, 'bet': bet})

    def update_balance(self, user_id: int, new_balance: int) -> ServiceResult[dict[str, Any]]:
        user = self._user_service.find_or_create(user_id)
        if not user:
            return ServiceResult.fail('No se pudo obtener el usuario.')

        self._user_service.update_user(user_id, balance=new_balance)
        return ServiceResult.ok({'balance': new_balance})

    def get_leaderboard(self, limit: int = 10) -> List[User]:
        return self._user_service.get_leaderboard(limit)
