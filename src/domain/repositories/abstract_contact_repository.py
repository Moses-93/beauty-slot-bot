from abc import ABC, abstractmethod
from src.domain.entities.contact import Contact


class AbstractContactRepository(ABC):
    """
    Abstract base class for contact repositories.
    """

    @abstractmethod
    async def get(self) -> Contact:
        """
        Retrieve a contact by its ID.
        """
        pass

    @abstractmethod
    async def create(self, contact: Contact) -> Contact:
        """
        Add a new contact.
        """
        pass

    @abstractmethod
    async def update(self, contact: Contact) -> Contact:
        """
        Update an existing contact.
        """
        pass

    @abstractmethod
    async def delete(self, contact_id: int) -> None:
        """
        Delete a contact by its ID.
        """
        pass
