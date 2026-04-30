from __future__ import annotations

import random
from typing import Protocol

from services.results import ServiceResult


class GameStrategyProtocol(Protocol):
    def execute(self, *args, **kwargs) -> ServiceResult[dict]:
        ...


class SlotStrategy(GameStrategyProtocol):
    def execute(self, bet: int) -> ServiceResult[dict]:
        emojis = ["🍒", "🍊", "🍋", "🍇", "🔔", "💎"]
        reels = [random.choice(emojis) for _ in range(3)]
        result_text = f"**[ {reels[0]} | {reels[1]} | {reels[2]} ]**"

        winnings = 0
        if reels[0] == reels[1] == reels[2]:
            winnings = bet * 10 if reels[0] == "💎" else bet * 5
        elif reels[0] == reels[1] or reels[1] == reels[2]:
            winnings = bet * 2

        return ServiceResult.ok({
            'result_text': result_text,
            'winnings': winnings,
            'bet': bet,
            'reels': reels,
        })


class CoinFlipStrategy(GameStrategyProtocol):
    def execute(self, choice: str, bet: int) -> ServiceResult[dict]:
        options = ['cara', 'cruz']
        result = random.choice(options)
        won = choice == result

        return ServiceResult.ok({
            'result': result,
            'won': won,
            'choice': choice,
            'bet': bet,
        })


class BlackjackStrategy(GameStrategyProtocol): # Implemented Blackjack Strategy
    def execute(
        self,
        player_value: int,
        dealer_value: int,
        bet: int,
        blackjack: bool = False,
    ) -> ServiceResult[dict]:
        change = 0
        description = ""
        color = 0x808080  # Default grey

        if blackjack:
            change = int(bet * 1.5)
            description = f'¡BLACKJACK! ¡Ganaste **{change}** monedas.'
            color = 0xFFD700  # Gold
        elif player_value > 21:
            change = -bet
            description = f'¡Te pasaste de 21! Pierdes **{bet}** monedas.'
            color = 0xFF0000  # Red
        elif dealer_value > 21 or player_value > dealer_value:
            change = bet
            description = f'¡Ganaste! Recibes **{bet}** monedas.'
            color = 0x00FF00  # Green
        elif player_value < dealer_value:
            change = -bet
            description = f'El crupier gana. Pierdes **{bet}** monedas.'
            color = 0xFF0000  # Red
        else:
            change = 0
            description = '¡Empate! Recuperas tu apuesta.'
            color = 0x808080  # Grey

        return ServiceResult.ok({
            'change': change,
            'description': description,
            'color': color,
        })
