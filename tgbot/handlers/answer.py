import logging
import random
import asyncio
from typing import Optional
from datetime import datetime, timedelta
from aiogram import Router, types, Bot, F
from aiogram.filters import CommandStart, CommandObject, StateFilter, Command
from aiogram.types import Message, CallbackQuery, FSInputFile, InlineKeyboardMarkup, InlineKeyboardButton, \
    KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove, InputMediaPhoto, InputMediaVideo
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from tgbot.keyboards.inline import answer_list_ikb, back_list, start_keyboard_user_db
from sqlalchemy import select, update
import redis.asyncio as redis
import json
import os


photo_menu = FSInputFile("tgbot/Support.png")
video_one = FSInputFile("tgbot/two.mp4")
video_two = FSInputFile("tgbot/first.mp4")
video_three = FSInputFile("tgbot/three.mp4")
video_four = FSInputFile("tgbot/four.mp4")


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
        media=InputMediaVideo(
            media=video_one,
            caption="<b>Натисніть на відео 👆\n\n</b>"
                    "<b>- Де Брати Документи\n\n</b>"
                    "Документи для завантаження автомобіля та додатковий ордер знаходяться на ваговій.Адресу можно "
                    "переглянути в розділі інструкції в профілі Teus Driver або при застосуванні цієї кнопки.\n\n"
                    "кнопка 'відкрити на мапі'(координаты весовой)"
        ),
        reply_markup=back_list()
    )


@answer_router.callback_query(F.data == "second")
async def answer_second(callback: CallbackQuery):
    await callback.message.edit_media(
        media=InputMediaVideo(
            media=video_two,
            caption="<b>Натисніть на відео 👆</b>\n\n"
                    "<b>- Де завантаження\n\n</b>"
                    "Інформацію щодо місця розвантаження/навантаження та марш"
                    "руту руху отримувати у експедитора/портового оператора\n\n,або у розділі відкритої заявки Teus "
                    "Drive "
        ),
        reply_markup=back_list()
    )


@answer_router.callback_query(F.data == "third")
async def answer_third(callback: CallbackQuery):
    await callback.message.edit_media(
        media=InputMediaVideo(
            media=video_three,
            caption="<b>Натисніть на відео 👆</b>\n\n"
                    "<b>- Куди мені їхати\n\n</b>"
                    "Рух до порту дозволено лише за наявності перепустки та товаро-транспортних документів.Перед "
                    "початком завантаження необхідно надіслати скан-копії документів. Документи для завантаження "
                    "автомобіля та додатковий ордер знаходяться на ваговій.Перед виїздом необхідно уточнити у "
                    "замовника адресу розташування КПП для в’їзду на територію порту/терміналу\n\n"
                    "або перевірити наявність QR-коду чи штрих-коду у розділі профілю додатку Teus Driver."
        ),
        reply_markup=back_list()
    )


@answer_router.callback_query(F.data == "four")
async def answer_four(callback: CallbackQuery):
    await callback.message.edit_media(
        media=InputMediaVideo(
            media=video_four,
            caption="<b>Натисніть на відео 👆\n\n</b>"
                    "<b>Що потрібно відправити для пропуску</b>\n\n"
                    "Рух до порту починати за наявності перепустки та товаро-транспортних документів. Перед "
                    "початком руху уточнити у замовника адресу розташування КПП для в’їзду на територію "
                    "порту/терміналу,\n\n або QR code чи Barcode у розділі профіля Teus Driver "
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



