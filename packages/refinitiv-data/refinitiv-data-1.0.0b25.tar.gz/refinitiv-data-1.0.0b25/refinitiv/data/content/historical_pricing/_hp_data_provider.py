# coding: utf8
from enum import Enum, unique
from functools import partial
from typing import Union, List, Optional

from .._content_provider import (
    HistoricalResponseFactory,
    HistoricalContentValidator,
    EventsDataProvider,
    SummariesDataProvider,
    get_fields_summaries,
    get_fields_events,
)
from .._content_type import ContentType
from .._intervals import (
    DayIntervalType,
    Intervals,
    get_day_interval_type,
    interval_arg_parser,
)
from ..._tools import (
    urljoin,
    make_enum_arg_parser,
    ParamItem,
    ValueParamItem,
    is_date_true,
)
from ..._tools._datetime import hp_datetime_adapter
from ...delivery._data._data_provider import (
    RequestFactory,
)


# --------------------------------------------------------------------------------------
#   EventTypes
# --------------------------------------------------------------------------------------


@unique
class EventTypes(Enum):
    """
    The list of market events (comma delimiter), supported event types are trade,
    quote and correction.
    Note: Currently support only single event type.
        If request with multiple event types,
        the backend will pick up the first event type to proceed.
    """

    TRADE = "trade"
    QUOTE = "quote"
    CORRECTION = "correction"


OptEventTypes = Optional[Union[str, List[str], EventTypes, List[EventTypes]]]
event_types_arg_parser = make_enum_arg_parser(EventTypes)


# --------------------------------------------------------------------------------------
#   Adjustments
# --------------------------------------------------------------------------------------


@unique
class Adjustments(Enum):
    """
    The list of adjustment types (comma delimiter) that tells the system whether
     to apply or not apply CORAX (Corporate Actions) events or
     exchange/manual corrections to historical time series data.

     The supported values of adjustments :

        UNADJUSTED - Not apply both exchange/manual corrections and CORAX
        EXCHANGE_CORRECTION - Apply exchange correction adjustment to historical pricing
        MANUAL_CORRECTION - Apply manual correction adjustment to historical pricing
                            i.e. annotations made by content analysts
        CCH - Apply Capital Change adjustment to historical Pricing due
              to Corporate Actions e.g. stock split
        CRE - Apply Currency Redenomination adjustment
              when there is redenomination of currency
        RPO - Apply Reuters Price Only adjustment
              to adjust historical price only not volume
        RTS - Apply Reuters TimeSeries adjustment
              to adjust both historical price and volume
        QUALIFIERS - Apply price or volume adjustment
              to historical pricing according to trade/quote qualifier
              summarization actions
    """

    UNADJUSTED = "unadjusted"
    EXCHANGE_CORRECTION = "exchangeCorrection"
    MANUAL_CORRECTION = "manualCorrection"
    CCH = "CCH"
    CRE = "CRE"
    RPO = "RPO"
    RTS = "RTS"
    QUALIFIERS = "qualifiers"


OptAdjustments = Optional[Union[str, List[str], Adjustments, List[Adjustments]]]
adjustments_arg_parser = make_enum_arg_parser(Adjustments)


# --------------------------------------------------------------------------------------
#   MarketSession
# --------------------------------------------------------------------------------------


@unique
class MarketSession(Enum):
    """
    The marketsession parameter represents a list of interested official durations
        in which trade and quote activities occur for a particular universe.

    The supported values of marketsession :

        PRE - specifies that data returned
              should include data during pre-market session
        NORMAL - specifies that data returned
                 should include data during normal market session
        POST - specifies that data returned
               should include data during post-market session
    """

    PRE = "pre"
    NORMAL = "normal"
    POST = "post"


OptMarketSession = Optional[Union[str, List[str], MarketSession, List[MarketSession]]]
market_sessions_arg_parser = make_enum_arg_parser(MarketSession)
# --------------------------------------------------------------------------------------
#   Intervals
# --------------------------------------------------------------------------------------


content_type_by_day_interval_type = {
    DayIntervalType.INTER: ContentType.HISTORICAL_PRICING_INTERDAY_SUMMARIES,
    DayIntervalType.INTRA: ContentType.HISTORICAL_PRICING_INTRADAY_SUMMARIES,
}


def get_content_type_by_interval(
    interval: Union[str, Intervals, DayIntervalType]
) -> ContentType:
    day_interval_type = get_day_interval_type(interval)
    return content_type_by_day_interval_type.get(day_interval_type)


def check_count(value):
    if value is not None and value < 1:
        raise ValueError("Count minimum value is 1")
    return value


hp_summaries_query_params = [
    ValueParamItem(
        "interval",
        function=interval_arg_parser.get_str,
    ),
    ValueParamItem("start", function=hp_datetime_adapter.get_str, is_true=is_date_true),
    ValueParamItem("end", function=hp_datetime_adapter.get_str, is_true=is_date_true),
    ValueParamItem(
        "adjustments",
        function=partial(adjustments_arg_parser.get_str, delim=","),
    ),
    ValueParamItem(
        "sessions",
        function=partial(market_sessions_arg_parser.get_str, delim=","),
    ),
    ValueParamItem("count", function=check_count),
    ParamItem("fields", function=get_fields_summaries),
]

hp_events_query_params = [
    ValueParamItem("interval", function=interval_arg_parser.get_str),
    ValueParamItem(
        "event_types", "eventTypes", partial(event_types_arg_parser.get_str, delim=",")
    ),
    ValueParamItem("start", function=hp_datetime_adapter.get_str, is_true=is_date_true),
    ValueParamItem("end", function=hp_datetime_adapter.get_str, is_true=is_date_true),
    ValueParamItem(
        "adjustments", function=partial(adjustments_arg_parser.get_str, delim=",")
    ),
    ValueParamItem("count", function=check_count),
    ParamItem("fields", function=get_fields_events),
]


# --------------------------------------------------------------------------------------
#   Request
# --------------------------------------------------------------------------------------


class HistoricalPricingRequestFactory(RequestFactory):
    def get_url(self, *args, **kwargs):
        url = args[1]
        url = urljoin(url, "/{universe}")
        return url

    def get_path_parameters(self, session=None, *, universe=None, **kwargs):
        if universe is None:
            return {}
        return {"universe": universe}

    def extend_body_parameters(self, body_parameters, extended_params=None, **kwargs):
        return None

    def extend_query_parameters(self, query_parameters, extended_params=None):
        if extended_params:
            query_parameters = dict(query_parameters)
            query_parameters.update(extended_params)
            for key in ("start", "end"):
                if key in extended_params:
                    arg_date = query_parameters[key]
                    query_parameters[key] = hp_datetime_adapter.get_str(arg_date)
            query_parameters = list(query_parameters.items())

        return query_parameters


class HistoricalPricingEventsRequestFactory(HistoricalPricingRequestFactory):
    @property
    def query_params_config(self):
        return hp_events_query_params


class HistoricalPricingSummariesRequestFactory(HistoricalPricingRequestFactory):
    @property
    def query_params_config(self):
        return hp_summaries_query_params


# --------------------------------------------------------------------------------------
#   Providers
# --------------------------------------------------------------------------------------

hp_events_data_provider = EventsDataProvider(
    request=HistoricalPricingEventsRequestFactory(),
    response=HistoricalResponseFactory(),
    validator=HistoricalContentValidator(),
)

hp_summaries_data_provider = SummariesDataProvider(
    request=HistoricalPricingSummariesRequestFactory(),
    response=HistoricalResponseFactory(),
    validator=HistoricalContentValidator(),
)
