from typing import Optional, Any, TYPE_CHECKING

from .._content_provider import ContentUsageLoggerMixin
from .._content_type import ContentType
from ..._tools import hp_universe_parser, validate_types
from ...delivery._data._data_provider import DataProviderLayer, BaseResponse, Data

if TYPE_CHECKING:
    from ._hp_data_provider import OptEventTypes, OptAdjustments
    from .._types import OptDateTime, StrStrings, OptInt, ExtendedParams, OptStrStrs


class Definition(
    ContentUsageLoggerMixin[BaseResponse[Data]], DataProviderLayer[BaseResponse[Data]]
):
    """
    Summary line of this class that defines parameters for requesting events from historical pricing

    Parameters
    ----------
    universe : str or list of str
        The entity universe
    eventTypes : list of EventTypes or EventTypes or str, optional
        The market events EventTypes
    start : str or date or datetime or timedelta, optional
        The start date and timestamp of the query in ISO8601 with UTC only
    end : str or date or datetime or timedelta, optional
        The end date and timestamp of the query in ISO8601 with UTC only
    adjustments : list of Adjustments or Adjustments or str, optional
        The adjustment list or Adjustments type
    count : int, optional
        The maximum number of data returned. Values range: 1 - 10000
    fields : list, optional
        The list of fields that are to be returned in the response
    closure : Any, optional
        Specifies the parameter that will be merged with the request
    extended_params : dict, optional
        If necessary other parameters

    Examples
    --------
    >>> from refinitiv.data.content.historical_pricing import events
    >>> definition_events = events.Definition("EUR")
    >>> response = definition_events.get_data()

    """

    def __init__(
        self,
        universe: "StrStrings",
        eventTypes: "OptEventTypes" = None,
        start: "OptDateTime" = None,
        end: "OptDateTime" = None,
        adjustments: "OptAdjustments" = None,
        count: "OptInt" = None,
        fields: "OptStrStrs" = None,
        closure: Optional[Any] = None,
        extended_params: "ExtendedParams" = None,
    ):
        universe = hp_universe_parser.get_list(universe)
        validate_types(count, [int, type(None)], "count")

        super().__init__(
            data_type=ContentType.HISTORICAL_PRICING_EVENTS,
            universe=universe,
            event_types=eventTypes,
            start=start,
            end=end,
            adjustments=adjustments,
            count=count,
            fields=fields,
            closure=closure,
            extended_params=extended_params,
        )
