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
                    "<b>- Що потрібно відправити для пропуску ❓\n\n</b>"
                    "Якщо ви їдете на погрузку для того щоб отримати перепустку "
                    "для навантаження або вигрузки необхідно відправити свої "
                    "дані (ПІП прописом, номери авто та причепа для навантаження а для вивантаження ще треба додати "
                    "фото  ТТН ) "
        ),
        reply_markup=back_list()
    )


@answer_router.callback_query(F.data == "second")
async def answer_second(callback: CallbackQuery):
    await callback.message.edit_media(
        media=InputMediaVideo(
            media=video_two,
            caption="<b>Натисніть на відео 👆</b>\n\n"
                    "<b>- Маршрут на вигрузку ❓\n\n</b>"
                    "Перед вигрузкою потрібно їхати до лабораторії після чого до "
                    "КПП №2 порту у м Чорноморьск  також можна подивитись"
                    "маршрут ну карті або в інструкції у додатку."
        ),
        reply_markup=back_list()
    )


@answer_router.callback_query(F.data == "third")
async def answer_third(callback: CallbackQuery):
    await callback.message.edit_media(
        media=InputMediaVideo(
            media=video_three,
            caption="<b>Натисніть на відео 👆</b>\n\n"
                    "<b>- Маршрут на погрузку❓\n\n</b>"
                    "Потрібно їхати до порту у м. Чорноморськ (КПП №2) також "
                    "можна подивитись маршрут ну карті або в інструкції у додатку."

        ),
        reply_markup=back_list()
    )


@answer_router.callback_query(F.data == "four")
async def answer_four(callback: CallbackQuery):
    await callback.message.edit_media(
        media=InputMediaVideo(
            media=video_four,
            caption="<b>Натисніть на відео 👆\n\n</b>"
                    "<b>Де брати документи на завантаження❓</b>\n\n"
                    "Документи для завантаження автомобіля та додатковий "
                    "ордер знаходяться на ваговій.Адресу можно переглянути в "
                    "розділі інструкції в профілі Teus Driver або при застосуванні цієї кнопки."
        ),
        reply_markup=back_list()
    )


@answer_router.callback_query(F.data == "five")
async def answer_five(callback: CallbackQuery):
    await callback.message.edit_media(
        media=InputMediaPhoto(
            media=photo_menu,
            caption="<b>Не працює навігація ❓</b>\n\n"
                    "Схема проїзда 1) лаба (вивантаження)- КПП №2 - Ваги та склади і причали (с геолокацієй)."
        ),
        reply_markup=back_list()
    )


# Обработчик для кнопки "Закрыть" - полностью удаляет сообщение
@answer_router.callback_query(F.data == "close")
async def close_message(callback: CallbackQuery):
    await callback.message.delete()





