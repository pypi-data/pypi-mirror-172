from dataclasses import dataclass
from typing import List, Optional, Union

from ...content._types import OptDateTime
from ...content.ipa._enums import PeriodType, DayCountBasis
from ...content.ipa.dates_and_calendars.count_periods import Definition


@dataclass
class CountedPeriods:
    count: float
    tenor: str


def count_periods(
    start_date: "OptDateTime" = None,
    end_date: "OptDateTime" = None,
    period_type: Optional[Union[PeriodType, str]] = None,
    calendars: Optional[List[str]] = None,
    currencies: Optional[List[str]] = None,
    day_count_basis: Optional[Union[DayCountBasis, str]] = None,
) -> CountedPeriods:
    """
    With this function you can get the period of time
    between a start date and an end date using one or many calendars.

    Parameters
    ----------
        start_date: str or datetime or timedelta, optional
            Start date of calculation.
        end_date: str or datetime or timedelta, optional
            End date of calculation.
        period_type : PeriodType or str, optional
            The method we chose to count the period of time based on value from PeriodType enumeration.
        calendars: list of str, optional
            Calendars to use the date for working day or weekend.
            Optional if currencies is provided.
        currencies: list of str, optional
            Currencies to use the date for working day or weekend.
            Optional if calendars is provided.
        day_count_basis: DayCountBasis or str, optional
            Day count basis value from DayCountBasis enumeration.

    Returns
    -------
    CountedPeriods
        Counted periods object with count and tenor values.

    Examples
    --------
     >>> import datetime
     >>> import refinitiv.data as rd
     >>> from refinitiv.data import dates_and_calendars
     >>>
     >>> rd.open_session("platform.default")
     >>>
     >>> counted_period = rd.dates_and_calendars.count_periods(
     ...    start_date=datetime.timedelta(-11),
     ...    end_date=datetime.timedelta(-3),
     ...    period_type=dates_and_calendars.PeriodType.WORKING_DAY,
     ...    currencies=["EUR"],
     >>>)
    """

    response = Definition(
        start_date=start_date,
        end_date=end_date,
        period_type=period_type,
        calendars=calendars,
        currencies=currencies,
        day_count_basis=day_count_basis,
    ).get_data()

    response = CountedPeriods(
        response.data.counted_period.count, response.data.counted_period.tenor
    )

    return response
