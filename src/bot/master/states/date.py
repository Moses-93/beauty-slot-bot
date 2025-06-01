from aiogram.fsm.state import State, StatesGroup


class DeactivateDateStates(StatesGroup):
    """
    This class defines states for the date deactivation process
    """

    date_id = State()


class CreateDateStates(StatesGroup):
    """
    This class defines states for the date creation process
    """

    date = State()
    deactivation_time = State()
