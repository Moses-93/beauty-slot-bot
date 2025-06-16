from enum import Enum


class PaginationCategory(str, Enum):
    SERVICES = "services"
    BOOKINGS = "bookings"
    DATES = "dates"
    CONTACTS = "contacts"
