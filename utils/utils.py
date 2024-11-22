import logging
from datetime import datetime
from db.db_writer import notes_manager
from bot.user.keyboards.booking_keyboard import confirm_time_keyboard
from cache.cache import user_cache
from .time_processing import check_slot, time_check, format_time
from .message_sender import manager
from .message_templates import template_manager
from os import getenv


USER_ID = getenv("USER_ID_ADMIN")


logger = logging.getLogger(__name__)


async def promote_booking(user_id: int, time: datetime):
    """Проміжна функція для запису в БД та відправлення повідомлень користувачу та майстру"""
    name, username, service, date = await user_cache.get_user_cache(
        user_id, "name", "username", "service", "date"
    )
    current_time = datetime.now()
    await notes_manager.create(
        name=name,
        username=username,
        time=time.time(),
        date_id=date.id,
        service_id=service.id,
        user_id=user_id,
        created_at=current_time,
    )
    msg_for_master = await template_manager.message_to_the_master(
        username,
        service.name,
        date.date,
        time.time(),
    )
    await manager.send_message(USER_ID, msg_for_master)
    msg_for_user = await template_manager.get_booking_confirmation(
        user_id=user_id,
        time=time.time(),
    )
    await manager.send_message(user_id, msg_for_user)


async def handlers_time(user_id: int, time: str):

    (date,) = await user_cache.get_user_cache(user_id, "date")
    time = format_time.formats_time_str_to_datetime(time).time()
    time = datetime.combine(date.date, time)
    if await time_check(time) == False:
        message = template_manager.elapsed_time_warning(time)
        return False, message
    nearest_time = await check_slot(user_id, time)
    if nearest_time == time:
        logger.info("Викликано функцію для запису в БД та відправки повідомлень")
        await promote_booking(
            user_id=user_id,
            time=time,
        )

    else:
        keyboard = confirm_time_keyboard(nearest_time)
        logger.info(
            f"Час, який обрав користувач - зайнятий, повернулась пропозиція з часом: {nearest_time}"
        )
        msg = template_manager.busy_time_notification(nearest_time.time())
        return (msg, keyboard)
