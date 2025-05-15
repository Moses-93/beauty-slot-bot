from aiogram.fsm.state import State, StatesGroup


class CreateServiceStates(StatesGroup):
    """
    This class defines states for the service creation process
    """

    title = State()
    price = State()
    duration = State()
