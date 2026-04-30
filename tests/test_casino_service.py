import pytest
from unittest.mock import MagicMock
import datetime
from services.casino_service import CasinoService
from models.user import User
from config import DAILY_AMOUNT

@pytest.fixture
def mock_user_service():
    return MagicMock()

@pytest.fixture
def casino_service(mock_user_service):
    return CasinoService(user_service=mock_user_service)

def test_validate_bet_insufficient_balance(casino_service, mock_user_service):
    # Configurar usuario con saldo insuficiente
    user_id = 123
    user = User(user_id=user_id, balance=50)
    mock_user_service.find_or_create.return_value = user

    # Ejecutar validación con apuesta de 100
    result = casino_service.validate_bet(user_id, 100)

    # Verificar que falle
    assert result.success is False
    assert "No tienes suficientes monedas" in result.error

def test_validate_bet_success(casino_service, mock_user_service):
    # Configurar usuario con saldo suficiente
    user_id = 123
    user = User(user_id=user_id, balance=500)
    mock_user_service.find_or_create.return_value = user

    # Ejecutar validación
    result = casino_service.validate_bet(user_id, 100)

    # Verificar éxito
    assert result.success is True
    assert result.data['balance'] == 500

def test_collect_daily_reward_success(casino_service, mock_user_service):
    user_id = 123
    now = datetime.datetime.now(datetime.timezone.utc)
    # Usuario que nunca ha reclamado (last_daily = None)
    user = User(user_id=user_id, balance=100, last_daily=None)
    mock_user_service.find_or_create.return_value = user
    mock_user_service.now_utc.return_value = now

    result = casino_service.collect_daily_reward(user_id, now=now)

    assert result.success is True
    assert result.data['balance'] == 100 + DAILY_AMOUNT
    # Verificar que se llamó a la actualización del usuario
    mock_user_service.update_user.assert_called_with(user_id, balance=100 + DAILY_AMOUNT, last_daily=now)

def test_collect_daily_reward_cooldown(casino_service, mock_user_service):
    user_id = 123
    now = datetime.datetime.now(datetime.timezone.utc)
    # Reclamó hace solo 1 hora
    last_claim = now - datetime.timedelta(hours=1)
    user = User(user_id=user_id, balance=100, last_daily=last_claim)
    mock_user_service.find_or_create.return_value = user
    mock_user_service.now_utc.return_value = now

    result = casino_service.collect_daily_reward(user_id, now=now)

    assert result.success is False
    assert "Aún no puedes reclamar" in result.error
    # Verificar que NO se actualizó el saldo
    mock_user_service.update_user.assert_not_called()

def test_coin_flip_win(casino_service, mock_user_service):
    user_id = 123
    bet = 100
    user = User(user_id=user_id, balance=200)
    mock_user_service.find_or_create.return_value = user
    
    # Forzamos a que la estrategia siempre gane para el test
    casino_service._coin_flip_strategy.execute = MagicMock(return_value=MagicMock(
        success=True, data={'won': True, 'result': 'cara', 'choice': 'cara'}
    ))

    result = casino_service.coin_flip(user_id, bet, 'cara')

    assert result.success is True
    assert result.data['won'] is True
    assert result.data['balance'] == 300 # 200 + 100
    mock_user_service.update_user.assert_called_with(user_id, balance=300)