from aiogram import F, Router
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, CallbackQuery
from .keyboards import services_keyboard, free_dates_list

router = Router()

@router.message(CommandStart())
async def start(message: Message):
    await message.answer(text='Привіт. \nЯ - майстер-бровіст Дарія.'
                         'Надаю професійні послуги з догляду за бровами.'
                         '\nОберіть будь ласка послугу:', reply_markup=services_keyboard)


@router.callback_query(lambda callback: callback.data == "correction")
async def handle_correction(callback: CallbackQuery):
    await callback.message.answer("Ви обрали Корекцію. Вартість: 200 грн. Введіть дату, на яку бажаєте записатись", reply_markup=free_dates_list)
    await callback.answer()  # Щоб закрити спливаюче вікно на клієнтській стороні