import logging

from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from ..middleware import AdminMiddleware
from ..states import AdminsForm
from ..keyboards.admin_keyboards import del_admin_button

from src.db.crud import admins_manager

from src.decorators.permissions import admin_only

from src.utils.formatted_view import ViewController


logger = logging.getLogger(__name__)

router = Router()
router.message.middleware(AdminMiddleware())
router.callback_query.middleware(AdminMiddleware())


@router.message(F.text == "Додати адміністратора")
@admin_only
async def start_command(message: Message, state: FSMContext, *args, **kwargs):
    await state.set_state(AdminsForm.name)
    msg = "Введіть ім'я адміністратора"
    await message.answer(text=msg)
    return


@router.message(F.text == "Видалити адміністратора")
@admin_only
async def delete_admin(message: Message, *args, **kwargs):
    admins = await admins_manager.read()
    if not admins:
        await message.answer(text="Список адміністраторів порожній.")
        return
    delete_keyboard = del_admin_button(admins=admins)
    await message.answer(
        text="Оберіть адміністратора для видалення", reply_markup=delete_keyboard
    )


@router.message(F.text == "Список адміністраторів")
@admin_only
async def show_admins(message: Message, *args, **kwargs):
    logger.info(f"Запуск обробника для показу списку адміністраторів")
    admins = await admins_manager.read()
    if not admins:
        await message.answer(text="Список адміністраторів порожній.")
        return
    admins_list = ViewController(admins=admins).get()
    await message.answer(text=admins_list, parse_mode="Markdown")
    return


@router.message(AdminsForm.name)
async def set_name(message: Message, state: FSMContext):
    name = message.text
    await state.update_data(name=name)
    msg = "Введіть chat_id адміністратора"
    await message.answer(text=msg)
    await state.set_state(AdminsForm.chat_id)


@router.message(AdminsForm.chat_id)
async def set_chat_id(message: Message, state: FSMContext):
    chat_id = int(message.text)
    data = await state.get_data()
    name = data.get("name")
    await admins_manager.create(name=name, chat_id=chat_id)
    await state.clear()
    msg = f"Адміністратор {name} зареєстрований у системі"
    await message.answer(text=msg)
    return


@router.callback_query(lambda c: c.data.startswith("del_admin_"))
async def del_admin(callback: CallbackQuery):
    id = int(callback.data.split("_")[2])
    await admins_manager.delete(id=id)
    msg = f"Адміністратор з ID: {id} був успішно видалений"
    await callback.message.answer(text=msg)
    await callback.answer()
