# coding: utf8

__all__ = ["HolidayOutputs"]

from enum import Enum, unique
from typing import Union, List, Optional


@unique
class HolidayOutputs(Enum):
    """
    Method to request additional information about the holiday.

    The possible values are:
        - Date (to retrieve holiday date),
        - Names (to retrieve holiday names.
            Holiday names might be different.
            It depends on counties and calendars.),
        - Calendars (to retrieve calendars for which this holidays belong),
        - Countries  (to retrieve countries for which this holidays belong).
    """

    DATE = "Date"
    NAMES = "Names"
    CALENDARS = "Calendars"
    COUNTRIES = "Countries"


OptHolidayOutputs = Optional[
    Union[str, List[str], HolidayOutputs, List[HolidayOutputs]]
]
