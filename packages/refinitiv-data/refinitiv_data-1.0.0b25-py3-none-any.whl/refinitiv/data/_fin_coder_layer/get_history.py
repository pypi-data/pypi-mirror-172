from datetime import date, datetime, timedelta
from logging import Logger
from typing import Dict, List, Optional, Union, Tuple, Sequence

from pandas import DataFrame

from ._containers import (
    UniverseContainer,
    FieldsContainer,
    ADCDataContainer,
    HPDataContainer,
    CustInstDataContainer,
)
from .context_collection import get_hp_context, get_adc_context, get_cust_inst_context
from ._history_provider_factory import get_history_provider
from ._intervals_consts import INTERVALS, EVENTS_INTERVALS
from .._core.session import get_default, is_open
from .._tools import (
    DEBUG,
    fr_datetime_adapter,
)
from ..content import (
    custom_instruments,
    fundamental_and_reference,
    historical_pricing,
)
from ..content._types import OptDateTime
from ..content.fundamental_and_reference._data_grid_type import (
    get_data_grid_type_by_session,
)
from ..usage_collection._filter_types import FilterType
from ..usage_collection._logger import get_usage_logger


def get_history(
    universe: Union[str, list],
    fields: Union[str, list, None] = None,
    interval: Optional[str] = None,
    start: "OptDateTime" = None,
    end: "OptDateTime" = None,
    adjustments: Optional[str] = None,
    count: Optional[int] = None,
    use_field_names_in_headers: Optional[bool] = False,
) -> DataFrame:
    """
    With this tool you can request historical data from Pricing and ADC

    Parameters
    ----------
        universe: str | list
            instruments to request.
        fields: str | list, optional
            fields to request.
        interval: str, optional
            The consolidation interval. Supported intervals are:
            tick, tas, taq, minute, 1min, 5min, 10min, 30min, 60min, hourly, 1h, daily,
            1d, 1D, 7D, 7d, weekly, 1W, monthly, 1M, quarterly, 3M, 6M, yearly, 1Y
        start: str or date or datetime or timedelta, optional
            The start date and timestamp of the query in ISO8601 with UTC only
        end: str or date or datetime or timedelta, optional
            The end date and timestamp of the query in ISO8601 with UTC only
        adjustments : str, optional
            The adjustment
        count : int, optional
            The maximum number of data returned. Values range: 1 - 10000
        use_field_names_in_headers : bool, optional
            Return field name in headers instead of title

    Returns
    -------
    pandas.DataFrame

     Examples
    --------
    >>> get_history(universe="GOOG.O")
    >>> get_history(universe="GOOG.O", fields="tr.Revenue", interval="1Y")
    >>> get_history(
    ...     universe="GOOG.O",
    ...     fields=["BID", "ASK", "tr.Revenue"],
    ...     interval="1Y",
    ...     start="2015-01-01",
    ...     end="2020-10-01",
    ... )
    """
    session = get_default()
    logger = session.logger()
    if not is_open(session):
        error_message = "Session is not opened. Can't send any request"
        logger.error(error_message)
        raise ValueError(error_message)

    if interval is not None and interval not in INTERVALS:
        raise ValueError(
            f"Not supported interval value.\nSupported intervals are:"
            f"{list(INTERVALS.keys())}"
        )

    # Library usage logging
    get_usage_logger().log_func(
        name=f"{__name__}.get_history",
        kwargs=dict(
            universe=universe,
            fields=fields,
            interval=interval,
            start=start,
            end=end,
            count=count,
            adjustments=adjustments,
            use_field_names_in_headers=use_field_names_in_headers,
        ),
        desc={FilterType.SYNC, FilterType.LAYER_ACCESS},
    )

    universe = UniverseContainer(universe)
    fields = FieldsContainer(fields)
    data_grid_type = get_data_grid_type_by_session(session)
    hp = get_hp_context(data_grid_type, universe, fields)
    adc = get_adc_context(data_grid_type, universe, fields)
    cust_inst = get_cust_inst_context(data_grid_type, universe, fields)

    adc_raw = None
    adc_df = None
    if adc.can_get_data:
        adc_params = get_adc_params(start, end, interval)
        adc_raw, adc_df = get_adc_data(
            universe=universe.adc,
            fields=fields.adc,
            parameters=adc_params,
            use_field_names_in_headers=use_field_names_in_headers,
            logger=logger,
        )

    adc_data = ADCDataContainer(adc_raw, adc_df, fields)
    universe.calc_hp(adc_data.raw)

    hp_raw = None
    hp_df = None
    if hp.can_get_data:
        hp_raw, hp_df = get_hp_data(
            universe=universe.hp,
            interval=interval,
            start=start,
            end=end,
            adjustments=adjustments,
            count=count,
            fields=fields.hp,
            logger=logger,
        )

    hp_data = HPDataContainer(hp_raw, hp_df)
    cust_inst_raw = None
    cust_inst_df = None
    if cust_inst.can_get_data:
        cust_inst_raw, cust_inst_df = get_custominsts_data(
            universe=universe.cust_inst,
            interval=interval,
            start=start,
            end=end,
            count=count,
            logger=logger,
        )
    cust_inst_data = CustInstDataContainer(cust_inst_raw, cust_inst_df)

    if not any({adc_data, hp_data, cust_inst_data}):
        return DataFrame()

    adc.set_data(adc_data, hp_data, cust_inst_data)
    hp.set_data(adc_data, hp_data, cust_inst_data)
    cust_inst.set_data(adc_data, hp_data, cust_inst_data)

    history_provider = get_history_provider(data_grid_type)
    return history_provider.get_df(
        adc, hp, cust_inst, universe, fields, interval, use_field_names_in_headers
    )


def get_hp_data(
    universe: List[str],
    fields: List[str],
    interval: Optional[str],
    start: Optional[str],
    end: Optional[str],
    adjustments: Optional[str],
    count: Optional[int],
    logger: Logger,
):
    """Get historical pricing raw data.

    Args:
        universe (List[str]): Sequence of RICs.
        fields (List[str]): List of fields for request.
        interval (Optional[str]): consolidation interval.
        start (Optional[str]): start date.
        end (Optional[str]): end date.
        adjustments (Optional[str]): adjustments for request.
        count (Optional[int]): the maximum number of data returned.
        logger (Logger): session logger.
    """
    if interval in EVENTS_INTERVALS:
        definition = historical_pricing.events.Definition(
            universe=universe,
            eventTypes=INTERVALS[interval]["event_types"],
            start=start,
            end=end,
            adjustments=adjustments,
            count=count,
            fields=fields,
        )

    else:
        interval = INTERVALS[interval]["pricing"] if interval is not None else interval

        definition = historical_pricing.summaries.Definition(
            universe=universe,
            interval=interval,
            start=start,
            end=end,
            adjustments=adjustments,
            count=count,
            fields=fields,
        )

    try:
        response = definition.get_data()
        DEBUG and logger.debug(
            f"HISTORICAL_PRICING --->\n{response.data.df.to_string()}\n"
        )
        raw = response.data.raw
        df = response.data.df
        return raw, df
    except Exception as e:
        if DEBUG:
            logger.exception(f"Failure sending request with {definition}, error:{e}")
        df = DataFrame()
        return {}, df


def get_adc_params(
    start: Union[str, date, datetime, timedelta],
    end: Union[str, date, datetime, timedelta],
    interval: Optional[str],
) -> dict:
    """Get parameters for ADC request.

    Args:
        start: start date for calculation parameters.
        end: end date for calculation parameters.
        interval: consolidated interval for calculation parameters.

    Returns:
        parameters: parameters for ADC request.
    """
    parameters = {}
    if start is not None:
        parameters["SDate"] = fr_datetime_adapter.get_str(start)

    if end is not None:
        parameters["EDate"] = fr_datetime_adapter.get_str(end)

    if interval is not None:
        parameters["FRQ"] = INTERVALS[interval]["adc"]

    return parameters


def get_adc_data(
    universe: List[str],
    fields: List[str],
    parameters: dict,
    use_field_names_in_headers: bool,
    logger: Logger,
) -> Union[Tuple[dict, DataFrame], Tuple[None, DataFrame]]:
    """Get ADC raw data.

    Args:
        universe (List[str]): sequence of RICs.
        fields (List[str]): list of fields for request.
        parameters (Dict[str]): precalculated parameters for request.
        use_field_names_in_headers (bool): return fields names in headers instead of title.
        logger (Logger): session logger.
    """
    definition = fundamental_and_reference.Definition(
        universe=universe,
        fields=fields,
        parameters=parameters,
        row_headers="date",
        use_field_names_in_headers=use_field_names_in_headers,
    )
    try:
        response = definition.get_data()
        raw = response.data.raw
        df = response.data.df
        DEBUG and logger.debug(f"ADC --->\n{response.data.df.to_string()}\n")
        return raw, df
    except Exception:
        if DEBUG:
            logger.exception(f"Failure sending request with {definition}")
        return {}, DataFrame()


def get_custominsts_data(
    universe: List[str],
    interval: Optional[str],
    start: Optional[str],
    end: Optional[str],
    count: Optional[int],
    logger: Logger,
) -> Union[Tuple[dict, DataFrame], Tuple[None, DataFrame]]:
    """Get custom instruments raw data.

    Args:
        universe (List[str]): list of RICs.
        interval (Optional[str]): optional interval.
        start (Optional[str]): optional start date.
        end (Optional[str]): optional end date.
        count (OptDict[int]): maximim number of retrieved data.
        logger (Logger): session logger.
    """
    if interval in EVENTS_INTERVALS:
        definition = custom_instruments.events.Definition(
            universe=universe,
            start=start,
            end=end,
            count=count,
        )

    else:
        interval = INTERVALS[interval]["pricing"] if interval is not None else interval
        definition = custom_instruments.summaries.Definition(
            universe=universe,
            interval=interval,
            start=start,
            end=end,
            count=count,
        )

    try:
        response = definition.get_data()
        raw = response.data.raw
        df = response.data.df
        DEBUG and logger.debug(f"CUSTOMINSTS --->\n{response.data.df.to_string()}\n")
        return raw, df
    except Exception:
        if DEBUG:
            logger.exception(f"Failure sending request with {definition}")
        return {}, DataFrame()
