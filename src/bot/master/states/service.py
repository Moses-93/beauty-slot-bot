from aiogram.fsm.state import State, StatesGroup


class CreateServiceStates(StatesGroup):
    """
    This class defines states for the service creation process
    """

    title = State()
    price = State()
    duration = State()


class DeleteServiceStates(StatesGroup):
    """
    This class defines states for the service deletion process
    """

    service_id = State()


class UpdateServiceStates(StatesGroup):
    """
    This class defines states for the service update process
    """

    service_id = State()
    title = State()
    price = State()
    duration = State()
