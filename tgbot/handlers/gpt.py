import logging
import asyncio
from datetime import datetime
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, FSInputFile, ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardButton
import os
from tgbot.config import load_config
import openai
from tgbot.keyboards.inline import get_exit_keyboard

config = load_config()

# Настройка логгера
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Настройка OpenAI
openai.api_key = config.tg_bot.openai

gpt_router = Router()
photo = FSInputFile("tgbot/Support.png")


# Состояния для чата с ИИ
class AIStates(StatesGroup):
    chatting = State()


# База знаний Teus
KNOWLEDGE_BASE = """
КОМПАНІЯ TEUS - ЛОГІСТИЧНА КОМПАНІЯ

=== О КОМПАНІЇ ===

Компанія TEUS працює у транспортно-логістичній галузі України з 2014 року, пропонуючи клієнтам комплексні мультимодальні логістичні рішення «під ключ», які охоплюють усі етапи логістичного процесу: від планування та організації перевезень до перевалки, зберігання та доставлення вантажів кінцевому отримувачу.

Ключові переваги TEUS:
- Комплексні мультимодальні логістичні рішення «під ключ»
- Мінімізація ризиків та забезпечення максимальної ефективності
- Широка географія співпраці в Україні та Європі
- Повний спектр логістичних послуг

=== СТРУКТУРА КОМПАНІЇ ===

Спеціалізовані відділи:
- Автотранспортний відділ - надійне та своєчасне перевезення вантажів
- Залізничний відділ - організація перевезень для великих обсягів та далекого транспортування
- Стивідорний відділ - перевалка вантажів у портах, швидка та ефективна обробка товарів
- Відділ фрахту та контейнерних перевезень - оптимальні рішення для морських перевезень
- Відділ трейдингу - допомога у закупівлях, продажу та обміну товарів на міжнародних ринках

=== ПАРТНЕРИ ТА ГЕОГРАФІЯ ===

У компанії є партнери в:
- Польщі
- Румунії
- Словаччині
- Угорщині
- Болгарії
- Країнах Балтії

=== РОЗВИТОК КОМПАНІЇ ===

Поточна діяльність:
- Оперує 800 орендованими вагонами
- Вже є 40 власних вагонів
- Заплановане придбання ще 70 власних вагонів
- Мета: сформувати парк з 300 вагонів

Плани розвитку:
- Побудувати власний портовий термінал
- Створити складські приміщення
- Відкрити лабораторію для аналізу аграрних вантажів
- Розвивати контейнерні та автоперевезення

У 2024 році розширили компетенції у сфері агротрейдингу, надаючи професійні брокерські послуги.

=== АВТОМОБІЛЬНІ ПЕРЕВЕЗЕННЯ ===

Послуги:
- Автоперевезення з/в країни Європи, країни колишнього СНД і середньої Азії
- Доставки комплексних і збірних вантажів
- Самоскиди під сипучі вантажі від 25 тонн
- Митне оформлення вантажів в режимі експорт та імпорт
- Доставки генеральних, небезпечних вантажів та відправлень з температурним режимом
- Доставки негабаритних і проектних вантажів
- Страхування вантажів

=== ПОРТОВА ЛОГІСТИКА ===

Спеціалізація на порті Чорноморськ:
- Комплексний підхід до портової логістики
- Планування і координація з судноплавними лініями
- Гарантований контроль якості зернових вантажів
- Сучасна інфраструктура і технічні можливості
- Гнучкі складські рішення
- Максимально ефективне навантаження і вивантаження
- Мінімізація простоїв і ризиків

Перевалка зернових вантажів у порту Чорноморськ - серце логістичної експертизи TEUS.

=== ПАМ'ЯТКА ДЛЯ ВОДІЯ (ПОРТ ЧОРНОМОРСЬК) ===

Основні вимоги:
1. Дотримуватись ПДР України та бути особливо уважними
2. Інформацію про місце розвантаження/навантаження отримувати у експедитора/портового оператора
3. Рух до порту - ТІЛЬКИ за наявності перепустки та товаро-транспортних документів
4. Уточнювати у замовника адресу КПП для в'їзду
5. Дотримуватись габаритно-вагових параметрів
6. Перевезення небезпечних вантажів - згідно з нормами законодавства
7. Швидкість у порту обмежена до 30 км/год
8. При повітряній тривозі КПП не працюють - прямувати до укриття!

КАТЕГОРИЧНО ЗАБОРОНЕНО:
- Зупинка/стоянка на вул. Перемоги та вул. Транспортна
- Стоянка біля КПП порту
- Технічне обслуговування, ремонт, мийка авто на території порту
- Засмічення проїжджої частини або узбіччя
- Користування відкритим вогнем

ПОКАРАННЯ: До порушників застосовуються заходи впливу, включно з забороною оформлення перепусток!

Додаткові рекомендації:
⚠️ Стежте за технічним станом автомобіля
⚠️ Перевіряйте документи на вантаж та автомобіль
⚠️ Забезпечте НАЛЕЖНЕ кріплення вантажу (не неналежне!)
⚠️ Дотримуйтесь швидкісного режиму в порту
⚠️ Фото/відеозйомка в порту заборонена
⚠️ Не вживайте алкоголь та наркотичні засоби
⚠️ Враховуйте погодні умови
⚠️ Не користуватися мобільним телефоном за кермом
"""

# Системный промпт для ИИ-ассистента
SYSTEM_PROMPT = f"""
Ти - віртуальний асистент логістичної компанії Teus. Ти допомагаєш водіям вантажівок.

ТВОЯ РОЛЬ:
- Досвідчений диспетчер та консультант з логістики
- Завжди готовий допомогти вирішити робочі питання
- Знаєш усі процедури та правила компанії Teus
- Говориш дружелюбно, але професійно
- Ти можешь відповідати на робочі запитання, якщо запитання особисті, або має не етичну норму спілкування, зроби попередження

БАЗА ЗНАНЬ КОМПАНІЇ:
{KNOWLEDGE_BASE}d

ПРАВИЛА ВІДПОВІДЕЙ:
1. Використовуй ТІЛЬКИ інформацію з бази знань вище
2. Відповідай коротко та по суті
3. При екстрених ситуаціях одразу давай номер диспетчера
4. Якщо не знаєш відповіді - направляй до диспетчера
5. Використовуй "ти" у спілкуванні
6. Додавай емодзі для кращого сприйняття
7. Завжди пропонуй додаткову допомогу

КРИТИЧНІ СИТУАЦІЇ (одразу давай контакти):
- ДТП, поломки, крадіжки
- Проблеми на кордоні
- Конфлікти з клієнтами
- Технічні несправності

Відповідай українською або російською мовою, як питає водій.

ВАЖЛИВО: Відповідай на тій мові, якою до тебе звертається водій - якщо питають українською, відповідай українською, якщо російською - російською.

СТИЛЬ СПІЛКУВАННЯ:
- Використовуй звертання "водію", "колего" для дружності
- Будь корисним та підтримуючим
- Давай конкретні поради та інструкції
- При проблемах - заспокоюй та направляй до вирішення
- Завжди нагадуй про безпеку на дорозі

ПРИКЛАДИ ВІДПОВІДЕЙ:
При екстреній ситуації: "🚨 НЕГАЙНО зв'яжись з диспетчером: +380XXXXXXXXX"
При звичайному питанні: "🚛 Допоможу! Ось що потрібно зробити..."
При завершенні: "✅ Ще щось потрібно? Безпечної дороги! 🛣️"
"""


@gpt_router.callback_query(F.data == "connect_ai")
async def start_ai_chat(callback: CallbackQuery, state: FSMContext):
    await callback.message.delete()

    # Инициализируем историю разговора с системным промптом
    conversation_history = [
        {"role": "system", "content": SYSTEM_PROMPT}
    ]

    # Сохраняем историю в состоянии FSM
    await state.update_data(conversation_history=conversation_history)

    welcome_text = """
**🤖 ІІ-Асистент Teus**
Привіт! Я твій віртуальний помічник. Можу відповісти на будь-які питання про роботу:
Просто напиши своє запитання...

"""

    await callback.message.answer(
        welcome_text,
        parse_mode="Markdown",
        reply_markup=get_exit_keyboard()
    )

    await state.set_state(AIStates.chatting)


@gpt_router.message(F.text == "☎️ Складне питання")
async def exit_ai_chat(message: Message, state: FSMContext):
    # Очищаем состояние (и историю разговора)
    await state.clear()

    # Убираем Reply клавиатуру
    await message.answer(
        "✅ **Чат з AI завершено**\n\n"
        "Перехід на звʼязок з нашим оператором\n",
        parse_mode="Markdown",
        reply_markup=ReplyKeyboardRemove()
    )

    kb = InlineKeyboardBuilder()
    kb.row(InlineKeyboardButton(text="Зв'язок з оператором", url="https://t.me/"))
    kb.row(InlineKeyboardButton(text="↩️ Назад у головне меню", callback_data="back_main"))

    await message.answer(
        "💬 **Потрібна допомога?**\nНатисніть кнопку та напишить нашому оператору",
        reply_markup=kb.as_markup()
    )


# Обработчик для кнопки выхода из чата
@gpt_router.message(F.text == "❌ Завершити чат з AI")
async def exit_ai_chat(message: Message, state: FSMContext):
    # Очищаем состояние (и историю разговора)
    await state.clear()

    # Убираем Reply клавиатуру
    await message.answer(
        "✅ **Чат з AI завершено**\n\n"
        "Дякую за використання AI-асистента Teus!\n"
        "Якщо знадобиться допомога - звертайся знову! 😊",
        parse_mode="Markdown",
        reply_markup=ReplyKeyboardRemove()
    )

    kb = InlineKeyboardBuilder()
    kb.row(InlineKeyboardButton(text="🤖 Відкрити AI-помічника", callback_data="connect_ai"))
    kb.row(InlineKeyboardButton(text="↩️ Назад у головне меню", callback_data="back_main"))

    await message.answer(
        "💬 **Потрібна допомога?**\nЗапитай у AI-асистента Teus!",
        reply_markup=kb.as_markup()
    )


@gpt_router.message(AIStates.chatting)
async def handle_ai_question(message: Message, state: FSMContext):
    user_question = message.text

    # Показываем, что бот печатает
    await message.bot.send_chat_action(message.chat.id, "typing")

    try:
        # Получаем историю разговора из состояния
        data = await state.get_data()
        conversation_history = data.get("conversation_history", [])

        # Если истории нет (например, при рестарте), создаем новую
        if not conversation_history:
            conversation_history = [
                {"role": "system", "content": SYSTEM_PROMPT}
            ]

        # Добавляем вопрос пользователя в историю
        conversation_history.append({
            "role": "user",
            "content": user_question
        })

        # Ограничиваем историю разговора (оставляем system + последние 20 сообщений)
        if len(conversation_history) > 21:  # system + 20 сообщений
            conversation_history = [conversation_history[0]] + conversation_history[-20:]

        # Отправляем запрос к OpenAI
        from openai import AsyncOpenAI

        client = AsyncOpenAI(api_key=openai.api_key)

        response = await client.chat.completions.create(
            model="gpt-4o-mini",  # Новая быстрая и дешевая модель
            messages=conversation_history,  # Отправляем всю историю
            max_tokens=800,
            temperature=0.3  # Меньше креативности, больше точности
        )

        ai_answer = response.choices[0].message.content

        # Добавляем ответ ассистента в историю
        conversation_history.append({
            "role": "assistant",
            "content": ai_answer
        })

        # Сохраняем обновленную историю в состоянии
        await state.update_data(conversation_history=conversation_history)

        # Отправляем ответ
        await message.answer(
            ai_answer,
            parse_mode="Markdown",
            reply_markup=get_exit_keyboard()
        )

        logger.info(f"AI response sent to user {message.from_user.id}")

    except Exception as e:
        logger.error(f"Error with OpenAI: {e}")

        await message.answer(
            f"❗ **Помилка AI-асистента**\n\n"
            f"📞 **Для термінової консультації:**\n"
            f"Диспетчерська: +380XXXXXXXXX (24/7)\n"
            f"Екстрена лінія: +380XXXXXXXXX",
            parse_mode="Markdown",
            reply_markup=get_exit_keyboard()
        )


# Функция для очистки старых разговоров (опционально)
async def cleanup_long_conversations(state: FSMContext):
    """Очищает слишком длинные разговоры для экономии памяти"""
    data = await state.get_data()
    conversation_history = data.get("conversation_history", [])

    # Если разговор слишком длинный, обрезаем его
    if len(conversation_history) > 50:
        # Оставляем system промпт + последние 30 сообщений
        conversation_history = [conversation_history[0]] + conversation_history[-30:]
        await state.update_data(conversation_history=conversation_history)
        logger.info("Conversation history cleaned up")


# Обработка сообщений вне чата (когда пользователь не в состоянии)
@gpt_router.message(F.text)
async def suggest_ai_help(message: Message):
    kb = InlineKeyboardBuilder()
    kb.add(InlineKeyboardButton(text="🤖 Відкрити AI-помічника", callback_data="connect_ai"))

    await message.answer(
        "💬 Чи є робоче питання? Запитай у AI-асистента Teus!",
        reply_markup=kb.as_markup()
    )


# Дополнительная функция для показа статистики разговора (для отладки)
@gpt_router.message(F.text.startswith("/debug_conversation"))
async def debug_conversation(message: Message, state: FSMContext):
    """Показывает информацию о текущем разговоре (только для отладки)"""
    data = await state.get_data()
    conversation_history = data.get("conversation_history", [])

    stats = f"""
🔍 **Debug информация:**
Сообщений в истории: {len(conversation_history)}
Состояние: {await state.get_state()}
Размер данных: {len(str(conversation_history))} символов
    """

    await message.answer(stats, parse_mode="Markdown")