import logging

from aiogram import F, Router
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, CallbackQuery
from .keyboards.keyboards import (
    services_keyboard,
    free_dates_keyboard,
    main_keyboard,
    notes,
    cancel_booking_button,
    create_reminder_keyboards,
    reminder_button,
)
from db.db_reader import GetService, GetNotes, GetFreeDate, DeleteNotes, UpdateNotes
from utils.utils import handlers_time, promote_booking
from decorators import (
    adding_user_data as add_usr_data,
    data_validation_in_user_data as check_user_data,
)
from user_data import get_user_data, set_user_data, user_data
from utils.message_sender import manager
from utils.message_templates import template_manager


logger = logging.getLogger(__name__)

router = Router()

time_pattern = r"^(1[0-7]:[0-5]\d|18:00)$"


@router.message(CommandStart())
async def start(message: Message, user_id):
    set_user_data(user_id)
    logger.info(f"USER_ID - {user_id}")
    msg = template_manager.get_greeting_message()
    await message.answer(text=msg, reply_markup=main_keyboard)


@router.message(lambda message: message.text == "Записатись")
async def make_an_appointment(message: Message):
    msg = template_manager.get_service_options()
    service = services_keyboard("service")
    await message.answer(text=msg, reply_markup=service)
    return


@router.message(lambda message: message.text == "Мої записи")
async def show_notes(message: Message):
    msg = template_manager.get_entry_options()
    await message.answer(text=msg, reply_markup=notes)
    return


@router.message(lambda message: message.text == "Послуги")
async def show_services(message: Message):
    formatted_service = "\n".join(
        [
            f"{i+1}: {service}"
            for i, service in enumerate(GetService().get_all_services())
        ]
    )

    await message.answer(text=f"Послуги:\n\n {formatted_service}")


@router.message(lambda message: message.text == "Контакти")
async def show_contacts(message: Message):
    msg = template_manager.get_contacts_info()
    await message.answer(text=msg, parse_mode="Markdown")


@router.callback_query(lambda c: c.data.startswith("all_notes"))
async def show_all_notes(callback: CallbackQuery, user_id):

    notes = GetNotes(user_id=user_id).get_all_notes()
    if notes:
        formatted_notes = "\n".join([f"{i+1}: {note}" for i, note in enumerate(notes)])
        await callback.message.answer(text=f"Всі записи: \n\n{formatted_notes}")
        await callback.answer()

    else:
        msg = template_manager.no_entries_found()
        await callback.message.answer(text=msg)
        await callback.answer()


@router.callback_query(lambda c: c.data.startswith("active_notes"))
async def show_active_notes(callback: CallbackQuery, user_id):

    active_notes = GetNotes(user_id=user_id, only_active=True).get_all_notes()
    cancel = cancel_booking_button(active_notes)
    logger.info(f"Active notes: {active_notes}")
    if active_notes:
        formatted_notes = "\n".join(
            [f"{note.id}: {note}" for i, note in enumerate(active_notes)]
        )
        await callback.message.answer(
            text=f"Активні записи: \n\n{formatted_notes}", reply_markup=cancel
        )
        await callback.answer()
    else:
        msg = template_manager.no_entries_found()
        await callback.message.answer(text=msg)
        await callback.answer()


@router.callback_query(lambda c: c.data.startswith("note_"))
async def cancel_booking(callback: CallbackQuery, user_id):
    note_id = int(callback.data.split("_")[1])
    (note,) = get_user_data(user_id, "note")
    if not note:
        msg = template_manager.booking_not_found()
        await callback.message.answer(text=msg)
        await callback.answer()
    else:
        msg_for_master = template_manager.get_booking_cancellation(note)
        await manager.send_message(user_id, message=msg_for_master)
        DeleteNotes(note_id=note_id).delete_note()
        msg = template_manager.get_cancel_notification()
        await callback.message.answer(text=msg)
        await callback.answer()


@router.callback_query(lambda c: c.data.startswith("service_"))
@add_usr_data.set_username
async def processes_services(callback: CallbackQuery, user_id, *args, **kwargs):
    service_id = int(callback.data.split("_")[2])
    service = GetService(service_id)

    logger.info(f"Selected date: {service.name}. Type:{type(service.name)}")
    msg = template_manager.service_selection_info(service)
    free_date = free_dates_keyboard("date")
    await callback.message.answer(
        text=msg,
        reply_markup=free_date,
    )
    set_user_data(user_id, service=service)
    logger.info(f"USER_DATA(handle_services) --- {get_user_data(user_id)}")
    await callback.answer()


@router.callback_query(lambda c: c.data.startswith("date_date_"))
@check_user_data.check_user_data(["service"])
async def processes_dates(callback: CallbackQuery, user_id, *args, **kwargs):
    date_id = int(callback.data.split("_")[2])
    date = GetFreeDate(date_id)
    logger.info(f"Selected date: {date.date}. Type:{type(date.date)}")
    msg = template_manager.date_selection_prompt(date)
    await callback.message.answer(text=msg)
    set_user_data(user_id, date=date)
    logger.info(f"USER_DATA(date_handler)---{get_user_data(user_id)}")
    await callback.answer()


@router.message(F.text.regexp(time_pattern))
@check_user_data.check_user_data(["date", "service"])
async def processes_time(message: Message, user_id, *args, **kwars):
    logger.debug("Запуск обробника часу")  # Логування початку виконання функції
    time = message.text
    logger.info(f"User selected time: {time}")
    logger.info(f"USER DATE(processes_time) -- {user_data}")
    handlers = await handlers_time(user_id, time)
    if handlers is None:
        service, date = get_user_data(user_id, "service", "date")
        msg = template_manager.successful_booking_notification(service, date, time)
        await message.answer(text=msg, reply_markup=reminder_button)
        # user_data.pop(user_id)
    elif handlers[0] == False:
        _, msg = handlers
        await message.answer(text=msg)
    else:
        message_text, keyboard = handlers
        await message.answer(text=message_text, reply_markup=keyboard)


@router.callback_query(lambda c: c.data.startswith("confirm_"))
async def confirm_the_entry(callback: CallbackQuery, user_id):
    time = callback.data.split("_")[-1]
    name, username, date, service = get_user_data(
        user_id, "name", "username", "date", "service"
    )
    await promote_booking(name, username, time, date, service, user_id)
    logger.info(f"SERVICE(in confirm_the_entry - {service})")
    msg = template_manager.successful_booking_notification(service, date, time)
    await callback.message.answer(text=msg, reply_markup=reminder_button)
    await callback.answer()
    # user_data.pop(user_id)


@router.callback_query(lambda c: c.data.startswith("show_reminder_button"))
async def offers_reminders(callback: CallbackQuery, user_id):
    (note_id,) = get_user_data(user_id, "note_id")
    logger.info(f"NOTE ID -- {note_id}")
    logger.info(f"USER DATA -- {user_data}")
    msg = template_manager.get_reminder()
    keyboard = create_reminder_keyboards(note_id)
    await callback.message.answer(text=msg, reply_markup=keyboard)
    await callback.answer()


@router.callback_query(lambda c: c.data.startswith("reminder_"))
async def process_reminder_callback(callback: CallbackQuery, user_id):
    logger.info(f"hour(int procces remonder -- {callback.data})")
    _, hour, note_id = callback.data.split("_")
    logger.info(f"User selected time: {hour}, {note_id}")
    UpdateNotes(note_id=note_id, reminder_hours=hour).update_reminder()
    msg = template_manager.get_reminder_notification(hour)
    await callback.message.answer(text=msg)
    await callback.answer()
    user_data.pop(user_id)
