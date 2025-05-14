from aiogram.fsm.state import State, StatesGroup


class DateStates(StatesGroup):
    """
    This class defines states for the date creation process
    """

    date = State()
    deactivation_time = State()
