from aiogram.fsm.state import State, StatesGroup


class ServiceForm(StatesGroup):
    name = State()
    price = State()
    duration = State()


class UpdateServiceForm(StatesGroup):
    field = State()


class FreeDateForm(StatesGroup):
    date = State()


class AdminsForm(StatesGroup):
    name = State()
    chat_id = State()
