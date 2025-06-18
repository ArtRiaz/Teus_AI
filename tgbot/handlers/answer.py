import logging
import random
import asyncio
from typing import Optional
from datetime import datetime, timedelta
from aiogram import Router, types, Bot, F
from aiogram.filters import CommandStart, CommandObject, StateFilter, Command
from aiogram.types import Message, CallbackQuery, FSInputFile, InlineKeyboardMarkup, InlineKeyboardButton, \
    KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove, InputMediaPhoto
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from tgbot.keyboards.inline import answer_list_ikb, back_list, start_keyboard_user_db
from sqlalchemy import select, update
import redis.asyncio as redis
import json
import os


photo_menu = FSInputFile("tgbot/Support.png")
photo_one = FSInputFile("tgbot/one.png")
photo_two = FSInputFile("tgbot/two.png")
photo_three = FSInputFile("tgbot/three.png")
photo_four = FSInputFile("tgbot/four.png")


answer_router = Router()


@answer_router.callback_query(F.data == "menu")
async def answer_list(callback: CallbackQuery):
    # Удаляем текущее сообщение и отправляем новое
    await callback.message.delete()
    await callback.message.answer_photo(
        photo_menu,
        caption="Telegram-Bot підтримки TEUS допомагає водіям швидко вирішити проблеми з робочими питаннями: від "
                "збоїв у програмі до специфікацій на замовленнях. Бот має готові відповіді на часті звернення та "
                "можливість миттєво контактувати з підтримкою - все в одному повідомленні без дзвінків.",
        reply_markup=answer_list_ikb()
    )


@answer_router.callback_query(F.data == "first")
async def answer_first(callback: CallbackQuery):
    # Редактируем существующее сообщение
    await callback.message.edit_media(
        media=InputMediaPhoto(
            media=photo_one,
            caption="На весовой, и прикрепить локацию, або дивитись в розділі маршрутна інструкція"
        ),
        reply_markup=back_list()
    )


@answer_router.callback_query(F.data == "second")
async def answer_second(callback: CallbackQuery):
    await callback.message.edit_media(
        media=InputMediaPhoto(
            media=photo_two,
            caption="Інформацію щодо місця розвантаження/навантаження та маршруту руху отримувати у "
                    "експедитора/портового оператора, або у розділі відкритої заявки Teus Driver "
        ),
        reply_markup=back_list()
    )


@answer_router.callback_query(F.data == "third")
async def answer_third(callback: CallbackQuery):
    await callback.message.edit_media(
        media=InputMediaPhoto(
            media=photo_three,
            caption="Рух до порту починати за наявності перепустки та товаро-транспортних документів. Перед "
                    "початком руху уточнити у замовника адресу розташування КПП для в’їзду на територію "
                    "порту/терміналу, або в розділі мапа Teus Driver "
        ),
        reply_markup=back_list()
    )


@answer_router.callback_query(F.data == "four")
async def answer_four(callback: CallbackQuery):
    await callback.message.edit_media(
        media=InputMediaPhoto(
            media=photo_four,
            caption="Рух до порту починати за наявності перепустки та товаро-транспортних документів. Перед "
                    "початком руху уточнити у замовника адресу розташування КПП для в’їзду на територію "
                    "порту/терміналу, або QR code чи Barcode у розділі профіля Teus Driver "
        ),
        reply_markup=back_list()
    )


@answer_router.callback_query(F.data == "five")
async def answer_five(callback: CallbackQuery):
    await callback.message.edit_media(
        media=InputMediaPhoto(
            media=photo_menu,
            caption="Зателефонуйте менеджеру або обирть кнопку дзвінка у розділі допомоги"
        ),
        reply_markup=back_list()
    )


# Обработчик для кнопки "Закрыть" - полностью удаляет сообщение
@answer_router.callback_query(F.data == "close")
async def close_message(callback: CallbackQuery):
    await callback.message.delete()


# Дополнительно: обработчик для кнопки "Назад" - удаляем сообщение
# @answer_router.callback_query(F.data == "back")
# async def back_to_menu(callback: CallbackQuery):
#     # Удаляем текущее сообщение
#     await callback.message.delete()
#
#     # Отправляем новое сообщение с главным меню
#     await callback.message.answer_photo(
#         photo,
#         caption="Description",
#         reply_markup=answer_list_ikb()
#     )



