from abc import ABC, abstractmethod


class GetNotesInterface(ABC):

    @abstractmethod
    async def get_notes(self, **filters):
        pass


class GetServicesInterface(ABC):

    @abstractmethod
    async def get_service(self, **filters):
        pass


class GetDatesInterface(ABC):

    @abstractmethod
    async def get_date(self, **filters):
        pass


class GetAdminsInterface(ABC):

    @abstractmethod
    async def get_admins(self, **filters):
        pass
