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

photo = FSInputFile("tgbot/app_main.png")

answer_router = Router()


@answer_router.callback_query(F.data == "menu")
async def answer_list(callback: CallbackQuery):
    # Удаляем текущее сообщение и отправляем новое
    await callback.message.delete()
    await callback.message.answer_photo(
        photo,
        caption="Description",
        reply_markup=answer_list_ikb()
    )


@answer_router.callback_query(F.data == "first")
async def answer_first(callback: CallbackQuery):
    # Редактируем существующее сообщение
    await callback.message.edit_media(
        media=InputMediaPhoto(
            media=photo,
            caption="Ответ на первый вопрос"
        ),
        reply_markup=back_list()
    )


@answer_router.callback_query(F.data == "second")
async def answer_second(callback: CallbackQuery):
    await callback.message.edit_media(
        media=InputMediaPhoto(
            media=photo,
            caption="Ответ на второй вопрос"
        ),
        reply_markup=back_list()
    )


@answer_router.callback_query(F.data == "third")
async def answer_third(callback: CallbackQuery):
    await callback.message.edit_media(
        media=InputMediaPhoto(
            media=photo,
            caption="Ответ на третий вопрос"
        ),
        reply_markup=back_list()
    )


@answer_router.callback_query(F.data == "four")
async def answer_four(callback: CallbackQuery):
    await callback.message.edit_media(
        media=InputMediaPhoto(
            media=photo,
            caption="Ответ на четвертый вопрос"
        ),
        reply_markup=back_list()
    )


@answer_router.callback_query(F.data == "five")
async def answer_five(callback: CallbackQuery):
    await callback.message.edit_media(
        media=InputMediaPhoto(
            media=photo,
            caption="Ответ на пятый вопрос"
        ),
        reply_markup=back_list()
    )


# Обработчик для кнопки "Закрыть" - полностью удаляет сообщение
@answer_router.callback_query(F.data == "close")
async def close_message(callback: CallbackQuery):
    await callback.message.delete()


# Дополнительно: обработчик для кнопки "Назад" - удаляем сообщение
@answer_router.callback_query(F.data == "back")
async def back_to_menu(callback: CallbackQuery):
    # Удаляем текущее сообщение
    await callback.message.delete()

    # Отправляем новое сообщение с главным меню
    await callback.message.answer_photo(
        photo,
        caption="Description",
        reply_markup=answer_list_ikb()
    )



