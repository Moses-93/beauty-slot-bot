from aiogram.fsm.state import State, StatesGroup


class ServiceForm(StatesGroup):
    name = State()
    price = State()
    durations = State()


class UpdateServiceForm(StatesGroup):
    field = State()


class FreeDateForm(StatesGroup):
    date = State()
