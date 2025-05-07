from abc import ABC, abstractmethod
from src.domain.entities.contact import Contact


class AbstractContactRepository(ABC):
    """
    Abstract base class for contact repositories.
    """

    @abstractmethod
    def get(self) -> Contact:
        """
        Retrieve a contact by its ID.
        """
        pass

    @abstractmethod
    def create(self, contact: Contact) -> Contact:
        """
        Add a new contact.
        """
        pass

    @abstractmethod
    def update(self, contact: Contact) -> Contact:
        """
        Update an existing contact.
        """

    pass

    @abstractmethod
    def delete(self, contact_id: int) -> None:
        """
        Delete a contact by its ID.
        """
        pass
