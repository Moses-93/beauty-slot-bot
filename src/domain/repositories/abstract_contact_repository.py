from abc import ABC, abstractmethod
from src.application.dto.contact import ContactDTO


class AbstractContactRepository(ABC):
    """
    Abstract base class for contact repositories.
    """

    @abstractmethod
    async def get(self) -> ContactDTO:
        """
        Retrieve a contact by its ID.
        """
        pass

    @abstractmethod
    async def create(self, contact: ContactDTO) -> ContactDTO:
        """
        Add a new contact.
        """
        pass

    @abstractmethod
    async def update(self, id: int, **kwargs) -> bool:
        """
        Update an existing contact.
        """
        pass

    @abstractmethod
    async def delete(self, contact_id: int) -> bool:
        """
        Delete a contact by its ID.
        """
        pass
