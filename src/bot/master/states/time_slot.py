from aiogram.fsm.state import State, StatesGroup


class CancelTimeSlotStates(StatesGroup):
    """
    This class defines states for the date deactivation process
    """

    time_slot_id = State()


class CreateTimeSlotStates(StatesGroup):
    """
    This class defines states for the date creation process
    """

    date = State()
    start_time = State()
    end_time = State()
