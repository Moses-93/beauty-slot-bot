from aiogram.fsm.state import State, StatesGroup


class DeleteDateStates(StatesGroup):
    """
    This class defines states for the date deletion process
    """

    date_id = State()


class CreateDateStates(StatesGroup):
    """
    This class defines states for the date creation process
    """

    date = State()
    deactivation_time = State()
