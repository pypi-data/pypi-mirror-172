import numpy as np
from typing import List, Optional, Union

from ...content._types import OptDateTime
from ...content.ipa._enums import DateMovingConvention, EndOfMonthConvention
from ...content.ipa.dates_and_calendars.add_periods import Definition


def add_periods(
    start_date: "OptDateTime" = None,
    period: str = None,
    calendars: Optional[List[str]] = None,
    currencies: Optional[List[str]] = None,
    date_moving_convention: Optional[Union[DateMovingConvention, str]] = None,
    end_of_month_convention: Optional[Union[EndOfMonthConvention, str]] = None,
) -> np.datetime64:
    """
    With this function you can add a time period to a given date using a given calendar.

    Parameters
    ----------
        start_date: str or datetime or timedelta, optional
            Start date of calculation.
        period: str, optional
            String representing the tenor.
        calendars: list of str, optional
            Calendars to use the date for working day or weekend.
            Optional if currencies is provided.
        currencies: list of str, optional
            Currencies to use the date for working day or weekend.
            Optional if calendars is provided.
        date_moving_convention : DateMovingConvention or str, optional
            The method to adjust dates.
        end_of_month_convention : EndOfMonthConvention or str, optional
            End of month convention.

    Returns
    -------
    np.datetime64
        Added period date

    Examples
    --------
     >>> import datetime
     >>> import refinitiv.data as rd
     >>> from refinitiv.data import dates_and_calendars
     >>>
     >>> rd.open_session("platform.default")
     >>>
     >>> added_period = rd.dates_and_calendars.add_periods(
     ...    start_date=datetime.date(2014, 1, 1),
     ...    period="1Y",
     ...    calendars=["BAR", "KOR"],
     ...    date_moving_convention=dates_and_calendars.DateMovingConvention.NEXT_BUSINESS_DAY,
     ...    end_of_month_convention=dates_and_calendars.EndOfMonthConvention.LAST28
     ... )
    """

    response = Definition(
        start_date=start_date,
        period=period,
        calendars=calendars,
        currencies=currencies,
        date_moving_convention=date_moving_convention,
        end_of_month_convention=end_of_month_convention,
    ).get_data()

    return np.datetime64(response.data.added_period.date)
