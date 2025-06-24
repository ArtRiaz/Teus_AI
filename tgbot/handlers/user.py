import logging
import random
import asyncio
from typing import Optional
from datetime import datetime, timedelta
from aiogram import Router, types, Bot, F
from aiogram.filters import CommandStart, CommandObject, StateFilter, Command
from aiogram.types import Message, CallbackQuery, FSInputFile, InlineKeyboardMarkup, InlineKeyboardButton, \
    KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from sqlalchemy import select, update
import redis.asyncio as redis
import json
import os

import aiohttp
from tgbot.keyboards.inline import start_keyboard_user, start_keyboard_user_db
from infrastructure.database.repo.requests import RequestsRepo
from infrastructure.database.model.user import User

import ssl

# Настройка логгера
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

auth_router = Router()

# Загружаем фото для стартового сообщения
photo = FSInputFile("tgbot/main.png")
video = FSInputFile("tgbot/IMG_5671.MP4")

data = [1064938479, "is_active"]

# auth_codes_storage = {}
#
# TURBOSMS_TOKEN = "1788d501ba72f6ef0274fe4fa0196539d80b177f"


# Состояния для авторизации
# class AuthStates(StatesGroup):
#     waiting_phone = State()
#     waiting_code = State()


caption_ukr = ("Компанія TEUS - це інтегратор та інноватор логістичних послуг, що розробляє комплексні логістичні "
               "рішення для ефективності бізнесу Клієнтів.\n\n"
               "Наша мета: спростити та зробити доступною міжнародну логістику для українських компаній, забезпечуючи "
               "стабільні та ефективні ланцюги постачання з будь-якої точки світу та в будь-яку точку світу.\n\n"
               "Для цього ми використовуємо інноваційні рішення, передові технології та сучасні підходи, щоб надати "
               "кожній компанії, незалежно від її масштабу, можливість керувати своїми ланцюгами постачання на рівні "
               "провідних світових гравців.")


@auth_router.message(CommandStart())
async def start(message: Message):
    user_id = message.from_user.id
    # await message.answer_video(video, caption=caption_ukr, reply_markup=start_keyboard_user_db())
    await message.answer_photo(photo, caption=caption_ukr, reply_markup=start_keyboard_user_db())


@auth_router.callback_query(F.data == "back_main")
async def answer_list(callback: CallbackQuery):
 
#    await callback.message.answer_video(video, caption=caption_ukr, reply_markup=start_keyboard_user_db())
    await callback.message.answer_photo(
         photo,
        caption=caption_ukr,
         reply_markup=start_keyboard_user_db()
    )
    await callback.message.answer_photo(photo, caption=caption_ukr, reply_markup=start_keyboard_user_db())
    

# @auth_router.callback_query(F.data == "auth")
# async def auth_system(callback: CallbackQuery, state: FSMContext):
#     await callback.message.answer(
#         "Введите свой номер телефона в формате +380XXXXXXXXX:"
#     )
#     await state.set_state(AuthStates.waiting_phone)

# @auth_router.message(AuthStates.waiting_phone)
# async def handle_phone_number(message: Message, state: FSMContext):
#     phone = message.text.strip()
#
#     # Исправляем проверку формата номера (для Украины)
#     if not phone.startswith("+380") or len(phone) != 13 or not phone[1:].isdigit():
#         await message.answer("Номер должен быть в формате +380XXXXXXXXX.")
#         return
#
#     code = random.randint(1000, 9999)
#     auth_codes_storage[message.from_user.id] = {
#         "code": str(code),
#         "expires": datetime.now() + timedelta(minutes=5)
#     }
#
#     # Создаём небезопасный SSL-контекст (временно, для теста)
#     ssl_context = ssl.create_default_context()
#     ssl_context.check_hostname = False
#     ssl_context.verify_mode = ssl.CERT_NONE
#
#     # Отправка СМС через TurboSMS согласно документации
#     async with aiohttp.ClientSession() as session:
#         headers = {
#             "Authorization": f"Bearer {TURBOSMS_TOKEN}",
#             "Content-Type": "application/json"
#         }
#
#         payload = {
#             "recipients": [phone],
#             "sms": {
#                 "text": f"Ваш код авторизации: {code}"
#             }
#         }
#
#         try:
#             async with session.post(
#                     "https://api.turbosms.ua/message/send.json",
#                     headers=headers,
#                     json=payload,
#                     ssl=ssl_context
#             ) as resp:
#                 response_text = await resp.text()
#                 logger.info(f"TurboSMS response status: {resp.status}")
#                 logger.info(f"TurboSMS response: {response_text}")
#
#                 if resp.status == 200:
#                     response_data = await resp.json() if resp.content_type == 'application/json' else None
#                     if response_data:
#                         logger.info(f"Response data: {response_data}")
#
#                     await message.answer("Код отправлен по СМС. Введите его:")
#                     await state.set_state(AuthStates.waiting_code)
#                 else:
#                     await message.answer(f"Ошибка при отправке СМС (код {resp.status}). Попробуйте позже.")
#                     logger.error(f"SMS sending failed: {resp.status} - {response_text}")
#
#         except Exception as e:
#             logger.error(f"Exception during SMS sending: {e}")
#             await message.answer("Ошибка при отправке СМС. Попробуйте позже.")
#
#
# # Функция для получения списка доступных отправителей SMS
# async def get_available_sms_senders():
#     """Получение списка доступных SMS отправителей"""
#     ssl_context = ssl.create_default_context()
#     ssl_context.check_hostname = False
#     ssl_context.verify_mode = ssl.CERT_NONE
#
#     async with aiohttp.ClientSession() as session:
#         headers = {"Authorization": f"Bearer {TURBOSMS_TOKEN}"}
#         try:
#             # Используем метод для получения отправителей
#             async with session.get(
#                     "https://api.turbosms.ua/user/senders.json",  # Этот endpoint может не существовать для SMS
#                     headers=headers,
#                     ssl=ssl_context
#             ) as resp:
#                 if resp.status == 200:
#                     data = await resp.json()
#                     logger.info(f"Available SMS senders: {data}")
#                     return data
#                 else:
#                     logger.error(f"SMS senders check failed: {resp.status}")
#                     response_text = await resp.text()
#                     logger.error(f"Response: {response_text}")
#                     return None
#         except Exception as e:
#             logger.error(f"Exception during SMS senders check: {e}")
#             return None
#
#
# # Функция для получения списка доступных отправителей
# async def get_available_senders():
#     """Получение списка доступных отправителей"""
#     ssl_context = ssl.create_default_context()
#     ssl_context.check_hostname = False
#     ssl_context.verify_mode = ssl.CERT_NONE
#
#     async with aiohttp.ClientSession() as session:
#         headers = {"Authorization": f"Bearer {TURBOSMS_TOKEN}"}
#         try:
#             async with session.get(
#                     "https://api.turbosms.ua/user/senders.json",
#                     headers=headers,
#                     ssl=ssl_context
#             ) as resp:
#                 if resp.status == 200:
#                     data = await resp.json()
#                     logger.info(f"Available senders: {data}")
#                     return data
#                 else:
#                     logger.error(f"Senders check failed: {resp.status}")
#                     return None
#         except Exception as e:
#             logger.error(f"Exception during senders check: {e}")
#             return None
#
#
# # Дополнительная функция для проверки баланса TurboSMS
# async def check_turbosms_balance():
#     """Проверка баланса в TurboSMS для диагностики"""
#     ssl_context = ssl.create_default_context()
#     ssl_context.check_hostname = False
#     ssl_context.verify_mode = ssl.CERT_NONE
#
#     async with aiohttp.ClientSession() as session:
#         headers = {"Authorization": f"Bearer {TURBOSMS_TOKEN}"}
#         try:
#             async with session.get(
#                     "https://api.turbosms.ua/user/balance.json",
#                     headers=headers,
#                     ssl=ssl_context
#             ) as resp:
#                 if resp.status == 200:
#                     data = await resp.json()
#                     logger.info(f"TurboSMS balance: {data}")
#                     return data
#                 else:
#                     logger.error(f"Balance check failed: {resp.status}")
#                     return None
#         except Exception as e:
#             logger.error(f"Exception during balance check: {e}")
#             return None
