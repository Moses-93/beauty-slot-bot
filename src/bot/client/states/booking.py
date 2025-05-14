from aiogram.fsm.state import State, StatesGroup


class BookingStates(StatesGroup):
    """
    This class defines the states for the booking process in a bot.
    Each state represents a step in the booking process.
    """

    service = State()
    date = State()
    time = State()
    reminder = State()
