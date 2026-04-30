import random
from typing import Any, Dict
from config import BOT_NAME

from services.results import ServiceResult
from models.user import User
from services.service_protocols import UserServiceProtocol


class EconomyService:
    def __init__(self, user_service: UserServiceProtocol) -> None:
        self._user_service = user_service

    def work(self, user_id: int) -> ServiceResult[Dict[str, Any]]:
        user = self._user_service.find_or_create(user_id)
        if not user:
            return ServiceResult.fail('No se pudo obtener el usuario.')

        cd = self._user_service.get_cooldown(user.last_work, 3600)
        if cd:
            return ServiceResult.fail(f'Estás cansado. Puedes volver a trabajar en {cd // 60}m {cd % 60}s.')

        earnings = random.randint(50, 200)
        jobs = [
            f"Ayudaste a {BOT_NAME} a limpiar el servidor.",
            "Programaste una nueva función para el bot.",
            "Vendiste limonada virtual.",
            "Trabajaste de moderador temporal.",
            "Paseaste a los perros del vecindario."
        ]
        job_desc = random.choice(jobs)
        new_balance = user.balance + earnings
        self._user_service.update_user(user_id, balance=new_balance, last_work=self._user_service.now_utc())

        return ServiceResult.ok({
            'balance': new_balance,
            'earnings': earnings,
            'job_desc': job_desc,
            'user': user
        })

    def crime(self, user_id: int) -> ServiceResult[Dict[str, Any]]:
        user = self._user_service.find_or_create(user_id)
        if not user:
            return ServiceResult.fail('No se pudo obtener el usuario.')

        cd = self._user_service.get_cooldown(user.last_crime, 10800)
        if cd:
            return ServiceResult.fail(f'La policía te está vigilando. Inténtalo de nuevo en {cd // 3600}h {(cd % 3600) // 60}m.')

        chance = random.randint(1, 100)
        if chance > 60:
            earnings = random.randint(300, 800)
            new_balance = user.balance + earnings
            message = f"😈 ¡Éxito! Robaste un banco virtual y escapaste con **{earnings}** monedas."
            color = 0x8B0000
        else:
            fine = min(random.randint(100, 300), user.balance)
            new_balance = user.balance - fine
            message = f"🚔 ¡Te atraparon! Tuviste que pagar una fianza de **{fine}** monedas."
            color = 0x99AAB5

        self._user_service.update_user(user_id, balance=new_balance, last_crime=self._user_service.now_utc())
        return ServiceResult.ok({
            'balance': new_balance,
            'message': message,
            'color': color,
        })

    def deposit(self, user_id: int, amount: int) -> ServiceResult[Dict[str, Any]]:
        if amount <= 0:
            return ServiceResult.fail('La cantidad debe ser positiva.')

        user = self._user_service.find_or_create(user_id)
        if not user:
            return ServiceResult.fail('No se pudo obtener el usuario.')

        wallet = user.balance
        bank = user.bank

        if wallet < amount:
            return ServiceResult.fail(f'No tienes suficiente dinero en la billetera. Tienes {wallet}.')

        self._user_service.update_user(user_id, balance=wallet - amount, bank=bank + amount)
        return ServiceResult.ok({'balance': wallet - amount, 'bank': bank + amount})

    def withdraw(self, user_id: int, amount: int) -> ServiceResult[Dict[str, Any]]:
        if amount <= 0:
            return ServiceResult.fail('La cantidad debe ser positiva.')

        user = self._user_service.find_or_create(user_id)
        if not user:
            return ServiceResult.fail('No se pudo obtener el usuario.')

        bank = user.bank
        if bank < amount:
            return ServiceResult.fail(f'No tienes suficiente dinero en el banco. Tienes {bank}.')

        self._user_service.update_user(user_id, balance=user.balance + amount, bank=bank - amount)
        return ServiceResult.ok({'balance': user.balance + amount, 'bank': bank - amount})

    def donate(self, from_id: int, to_id: int, amount: int) -> ServiceResult[Dict[str, Any]]:
        if amount <= 0:
            return ServiceResult.fail('La cantidad a donar debe ser mayor a 0.')

        if from_id == to_id:
            return ServiceResult.fail('No puedes donarte monedas a ti mismo.')

        giver = self._user_service.find_or_create(from_id)
        receiver = self._user_service.find_or_create(to_id)
        if not giver or not receiver:
            return ServiceResult.fail('No se pudo obtener la información de usuario.')

        if giver.balance < amount:
            return ServiceResult.fail(f'No tienes suficientes monedas. Tu saldo actual es de {giver.balance}.')

        self._user_service.update_user(from_id, balance=giver.balance - amount)
        self._user_service.update_user(to_id, balance=receiver.balance + amount)
        return ServiceResult.ok({
            'message': f"Has transferido **{amount}** monedas a <@{to_id}>.",
            'balance': giver.balance - amount,
            'receiver_balance': receiver.balance + amount
        })

    def rob(self, from_id: int, to_id: int) -> ServiceResult[Dict[str, Any]]:
        if from_id == to_id:
            return ServiceResult.fail('No puedes robarte a ti mismo.')

        thief = self._user_service.find_or_create(from_id)
        victim = self._user_service.find_or_create(to_id)
        if not thief or not victim:
            return ServiceResult.fail('No se pudo obtener la información de los usuarios.')

        if victim.balance < 50:
            return ServiceResult.fail('La víctima tiene muy poco dinero para robar.')

        cd = self._user_service.get_cooldown(thief.last_crime, 7200)
        if cd:
            return ServiceResult.fail(f'Estás en enfriamiento. Puedes intentar robar de nuevo en {cd // 3600}h {(cd % 3600) // 60}m.')

        success_chance = random.randint(1, 100)
        if success_chance > 70:
            steal_amount = random.randint(10, int(victim.balance * 0.5))
            self._user_service.update_user(from_id, balance=thief.balance + steal_amount, last_crime=self._user_service.now_utc())
            self._user_service.update_user(to_id, balance=victim.balance - steal_amount)
            return ServiceResult.ok({
                'success': True,
                'message': f"🕵️‍♂️ ¡Le has robado **{steal_amount}** monedas a <@{to_id}>!",
                'stolen': steal_amount,
                'victim_id': to_id
            })

        fine = min(200, thief.balance)
        self._user_service.update_user(from_id, balance=thief.balance - fine, last_crime=self._user_service.now_utc())
        return ServiceResult.ok({
            'success': False,
            'message': f"🚔 ¡Te atraparon intentando robar a <@{to_id}>! Pagaste una multa de **{fine}** monedas.",
            'fine': fine
        })
