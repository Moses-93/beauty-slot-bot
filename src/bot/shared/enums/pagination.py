from enum import Enum


class PaginationCategory(str, Enum):
    SERVICES = "services"
    ALL_BOOKINGS = "all_bookings"
    ACTIVE_BOOKINGS = "active_bookings"
    DATES = "dates"
    CONTACTS = "contacts"
