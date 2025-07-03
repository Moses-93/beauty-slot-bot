from dataclasses import dataclass, field
from datetime import datetime, time, date as Date
from typing import Optional


@dataclass(kw_only=True)
class DateSlot:
    id: Optional[int] = field(default=None)
    date: Date
    deactivation_time: time
    is_active: bool = field(default=False)

    def is_past(self) -> bool:
        """
        Check if the date is in the past compared to the current time.
        """
        now = datetime.now()
        return self.date < now.date() or (
            self.date == now.date() and self.deactivation_time < now.time()
        )

    @classmethod
    def create(
        cls,
        date: Date,
        deactivation_time: time,
        id: Optional[int] = None,
        is_active: bool = True,
    ) -> "Date":
        """Created a new Date instance.

        Args:
            date (Date):
            deactivation_time (time): A time when the date will be deactivated.
            id (Optional[int], optional): Date identifier in the database. Defaults to None.
            is_active (bool, optional): Indicates whether the date is currently active. Defaults to True.

        Raises:
            ValueError: If the deactivation date or time is in the past, an error is raised.

        Returns:
            Date: A new Date instance.
        """
        now = datetime.now()
        if date < now.today():
            raise ValueError(
                "Date cannot be in the past"
            )  # TODO: Add custom exception and message
        if date == now.today() and deactivation_time < now.time():
            raise ValueError(
                "Deactivation time cannot be in the past"
            )  # TODO: Add custom exception and message
        return cls(
            id=id, date=date, deactivation_time=deactivation_time, is_active=is_active
        )

    def deactivate(self) -> None:
        """
        Deactivate the date.
        """
        if not self.is_active:
            raise ValueError(
                "Date is already inactive"
            )  # TODO: Add custom exception and message
        self.is_active = False
