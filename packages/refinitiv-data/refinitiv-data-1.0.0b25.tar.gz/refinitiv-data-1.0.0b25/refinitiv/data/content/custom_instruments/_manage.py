import warnings
from typing import Optional, List, Union

from ._enums import CustomInstrumentTypes
from ._instrument_class import (
    create_instr_factory,
    CustomInstrumentFormula,
    CustomInstrumentBasket,
    CustomInstrumentUDC,
)
from ._instrument_prop_classes import Basket, UDC
from .._content_type import ContentType
from .._types import ExtendedParams
from ..ipa.dates_and_calendars.holidays._holidays_data_provider import Holiday
from ...delivery._data._data_provider import DataProviderLayer, Response
from ...delivery._data._endpoint_data import RequestMethod


def delete(
    universe,
    extended_params: "ExtendedParams" = None,
    session=None,
) -> Response:
    """
    universe : str
        Instrument symbol in the format "S)someSymbol.YOURUUID".
    extended_params : ExtendedParams, optional
        If necessary other parameters.

    Examples
    --------
    >>> from refinitiv.data.content.custom_instruments.manage import delete
    >>> response = delete("MyInstrument")
    """
    data_provider_layer = DataProviderLayer(
        data_type=ContentType.CUSTOM_INSTRUMENTS_INSTRUMENTS,
        universe=universe,
        extended_params=extended_params,
    )
    return data_provider_layer.get_data(session, method=RequestMethod.DELETE)


def get(
    universe, extended_params: "ExtendedParams" = None, session=None
) -> Union[CustomInstrumentFormula, CustomInstrumentBasket, CustomInstrumentUDC]:
    """
    universe : str
        Instrument symbol in the format "S)someSymbol.YOURUUID".
    extended_params : ExtendedParams, optional
        If necessary other parameters.

    Examples
    --------
    >>> from refinitiv.data.content.custom_instruments.manage import get
    >>> response = get("MyInstrument")
    """
    data_provider_layer = DataProviderLayer(
        data_type=ContentType.CUSTOM_INSTRUMENTS_INSTRUMENTS, universe=universe
    )
    response = data_provider_layer.get_data(
        method=RequestMethod.GET, extended_params=extended_params, session=session
    )
    return create_instr_factory(response.data.raw, session=session)


# deprecated method
def create(
    symbol: str,
    formula: Optional[str] = None,
    basket: Optional[dict] = None,
    udc: Optional[dict] = None,
    instrument_name: Optional[str] = None,
    exchange_name: Optional[str] = None,
    currency: Optional[str] = None,
    time_zone: Optional[str] = None,
    holidays: Optional[List[Union[dict, Holiday]]] = None,
    description: Optional[str] = None,
    type_: Union[str, CustomInstrumentTypes] = CustomInstrumentTypes.Formula,
    extended_params: "ExtendedParams" = None,
    session=None,
    on_response=None,
) -> Union[CustomInstrumentFormula, CustomInstrumentBasket, CustomInstrumentUDC]:
    """
    With this method you can create a CustomInstrumentFormula, CustomInstrumentBasket, CustomInstrumentUDC objects.

    Parameters
    ----------
    symbol: str
        Instrument symbol in the format "S)someSymbol.YOURUUID".
    formula : str
        Formula consisting of rics (fields can be specified by comma).
    basket : dict, Basket, optional
        Method of defining custom instruments, relying on a list of instruments and weights in order to build
        custom indices or other simple synthetic instruments
    udc : dict, UDC, optional
        User-Defined Continuations. Custom trading sessions, see sample format below.
    currency : str, optional
        3-letter code of the currency of the instrument, e.g. GBP.
    instrument_name : str, optional
        Human-readable name of the instrument. Maximum of 16 characters.
    exchange_name : str, optional
        4-letter code of the listing exchange.
    holidays : list[dict, Holiday], optional
        List of custom calendar definitions.
    time_zone : str, optional
        Time Series uses an odd custom 3-letter value for time zone IDs, e.g. "LON" for London.
    description : str, optional
        Free text field from the user to put any notes or text. Up to 1000 characters.
    type_ : str, CustomInstrumentTypes, optional
        Type of Synthetic Instrument - "formula", "basket","udc". Default value is "formula".
    extended_params : ExtendedParams, optional
        If necessary other parameters.

    Returns
    -------
        CustomInstrumentFormula

    Examples
    --------
    >>> from refinitiv.data.content.custom_instruments.manage import create_formula
    >>> import refinitiv.data.content.custom_instruments as ci
    >>> from refinitiv.data.content.ipa import dates_and_calendars
    >>> calendar_holiday = dates_and_calendars.holidays.Definition(
    ...     start_date="2015-08-24",
    ...     end_date="2018-09-24",
    ...     calendars=["UKR"],
    ...     holiday_outputs=["Date", "Names"],
    >>> ).get_data()
    ...
    >>> response = create_formula(
    ...     symbol="MyNewInstrument",
    ...     formula="EUR=*3",
    ...     holidays=[
    ...         *calendar_holiday.data.holidays,
    ...         ci.manage.Holiday(date="1991-08-24", name="Independence Day of Ukraine"),
    ...         {"date": "2022-12-18", "reason": "Hanukkah"},
    ...     ],
    >>> )
    """
    warnings.warn(
        "'create()' is legacy interface. "
        "Will be changed to 'create_formula()', 'create_basket()', 'create_udc()'",
    )
    data = _create(
        symbol,
        formula,
        basket,
        udc,
        instrument_name,
        exchange_name,
        currency,
        time_zone,
        holidays,
        description,
        type_,
        extended_params,
        session,
        on_response,
    )
    return create_instr_factory(data, session=session)


def _create(
    symbol: str,
    formula: Optional[str] = None,
    basket: Union[dict, Basket] = None,
    udc: Union[dict, UDC] = None,
    instrument_name: Optional[str] = None,
    exchange_name: Optional[str] = None,
    currency: Optional[str] = None,
    time_zone: Optional[str] = None,
    holidays: Optional[List[Union[dict, Holiday]]] = None,
    description: Optional[str] = None,
    type_: Union[str, CustomInstrumentTypes] = None,
    extended_params: "ExtendedParams" = None,
    session=None,
    on_response=None,
) -> dict:

    data_provider_layer = DataProviderLayer(
        data_type=ContentType.CUSTOM_INSTRUMENTS_INSTRUMENTS,
        symbol=symbol,
        formula=formula,
        instrument_name=instrument_name,
        exchange_name=exchange_name,
        currency=currency,
        time_zone=time_zone,
        holidays=holidays,
        description=description,
        type_=type_,
        basket=basket,
        udc=udc,
        extended_params=extended_params,
    )
    response = data_provider_layer.get_data(
        session, on_response, method=RequestMethod.POST
    )
    return response.data.raw


def create_formula(
    symbol: str,
    formula: Optional[str] = None,
    currency: Optional[str] = None,
    instrument_name: Optional[str] = None,
    exchange_name: Optional[str] = None,
    holidays: Optional[List[Union[dict, Holiday]]] = None,
    time_zone: Optional[str] = None,
    description: Optional[str] = None,
    extended_params: "ExtendedParams" = None,
    session=None,
    on_response=None,
):
    """
    With this method you can create a CustomInstrumentFormula object.

    Parameters
    ----------
    symbol: str
        Instrument symbol in the format "S)someSymbol.YOURUUID".
    formula : str
        Formula consisting of rics (fields can be specified by comma).
    currency : str, optional
        3-letter code of the currency of the instrument, e.g. GBP.
    instrument_name : str, optional
        Human-readable name of the instrument. Maximum of 16 characters.
    exchange_name : str, optional
        4-letter code of the listing exchange.
    holidays : list[dict, Holiday], optional
        List of custom calendar definitions.
    time_zone : str, optional
        Time Series uses an odd custom 3-letter value for time zone IDs, e.g. "LON" for London.
    description : str, optional
        Free text field from the user to put any notes or text. Up to 1000 characters.
    extended_params : ExtendedParams, optional
        If necessary other parameters.

    Returns
    -------
        CustomInstrumentFormula

    Examples
    --------
    >>> from refinitiv.data.content.custom_instruments.manage import create_formula
    >>> import refinitiv.data.content.custom_instruments as ci
    >>> response = create_formula(
    ...     symbol="MyNewInstrument",
    ...     formula="EUR=*3",
    ...     holidays=[
    ...         ci.manage.Holiday(date="1991-08-23", name="Independence Day of Ukraine"),
    ...         {"date": "2022-12-18", "reason": "Hanukkah"},
    ...     ],
    >>> )
    """
    data = _create(
        symbol=symbol,
        type_=CustomInstrumentTypes.Formula,
        formula=formula,
        currency=currency,
        instrument_name=instrument_name,
        exchange_name=exchange_name,
        holidays=holidays,
        time_zone=time_zone,
        description=description,
        extended_params=extended_params,
        session=session,
        on_response=on_response,
    )
    return CustomInstrumentFormula(data, session=session)


def create_basket(
    symbol: str,
    basket: Union[dict, Basket],
    currency: str,
    instrument_name: Optional[str] = None,
    exchange_name: Optional[str] = None,
    holidays: Optional[List[Union[dict, Holiday]]] = None,
    time_zone: Optional[str] = None,
    description: Optional[str] = None,
    extended_params: "ExtendedParams" = None,
    session=None,
    on_response=None,
):
    """
    With this method you can create a CustomInstrumentBasket object.

    Parameters
    ----------
    symbol: str
        Instrument symbol in the format "S)someSymbol.YOURUUID".
    basket : dict, Basket
        Method of defining custom instruments, relying on a list of instruments and weights in order to build
        custom indices or other simple synthetic instruments
    currency : str
        3-letter code of the currency of the instrument, e.g. GBP.
    instrument_name : str, optional
        Human-readable name of the instrument. Maximum of 16 characters.
    exchange_name : str, optional
        4-letter code of the listing exchange.
    holidays : list[dict, Holiday], optional
        List of custom calendar definitions.
    time_zone : str, optional
        Time Series uses an odd custom 3-letter value for time zone IDs, e.g. "LON" for London.
    description : str, optional
        Free text field from the user to put any notes or text. Up to 1000 characters.
    extended_params : ExtendedParams, optional
        If necessary other parameters.

    Returns
    -------
        CustomInstrumentBasket

    Examples
    --------
    >>> from refinitiv.data.content.custom_instruments.manage import create_basket
    >>> import refinitiv.data.content.custom_instruments as ci
    ... response = create_basket(
    ...        symbol="MyBasketInstrument",
    ...        basket=Basket(
    ...            constituents=[
    ...                ci.manage.Constituent(ric="LSEG.L", weight=50),
    ...                ci.manage.Constituent(ric="EPAM.N", weight=50),
    ...            ],
    ...            normalize_by_weight=True,
    ...        ),
    ...        currency="USD",
    ...    )
    """

    data = _create(
        symbol=symbol,
        type_=CustomInstrumentTypes.Basket,
        basket=basket,
        currency=currency,
        instrument_name=instrument_name,
        exchange_name=exchange_name,
        holidays=holidays,
        time_zone=time_zone,
        description=description,
        extended_params=extended_params,
        session=session,
        on_response=on_response,
    )
    return CustomInstrumentBasket(data, session=session)


def create_udc(
    symbol,
    udc: Union[dict, UDC],
    currency: Optional[str] = None,
    instrument_name: Optional[str] = None,
    exchange_name: Optional[str] = None,
    holidays: Optional[List[Union[dict, Holiday]]] = None,
    time_zone: Optional[str] = None,
    description: Optional[str] = None,
    extended_params: "ExtendedParams" = None,
    session=None,
    on_response=None,
):
    """
    With this method you can create a CustomInstrumentUDC object.

    Parameters
    ----------
    symbol: str
        Instrument symbol in the format "S)someSymbol.YOURUUID".
    udc : dict, UDC
        User-Defined Continuations. Custom trading sessions, see sample format below.
    currency : str, optional
        3-letter code of the currency of the instrument, e.g. GBP.
    instrument_name : str, optional
        Human-readable name of the instrument. Maximum of 16 characters.
    exchange_name : str, optional
        4-letter code of the listing exchange.
    holidays : list[dict, Holiday], optional
        List of custom calendar definitions.
    time_zone : str, optional
        Time Series uses an odd custom 3-letter value for time zone IDs, e.g. "LON" for London.
    description : str, optional
        Free text field from the user to put any notes or text. Up to 1000 characters.
    extended_params : ExtendedParams, optional
        If necessary other parameters.

    Returns
    -------
        CustomInstrumentBasket

    Examples
    --------
    >>> from refinitiv.data.content.custom_instruments.manage import create_udc
    >>> import refinitiv.data.content.custom_instruments as ci
    ...
    >>> response_1 = create_udc(
    ...     symbol="MyUDCInstrument_VB",
    ...     instrument_name="Co Systems Inc",
    ...     udc=ci.manage.UDC(
    ...         root="CC",
    ...         months=ci.manage.Months(
    ...             number_of_years=3,
    ...             include_all_months=True,
    ...             start_month=1,
    ...         ),
    ...         rollover=ci.manage.VolumeBasedRollover(
    ...             method=ci.VolumeBasedRolloverMethod.VOLUME,
    ...             number_of_days=1,
    ...             join_at_day=1,
    ...             roll_occurs_within_months=4,
    ...             roll_on_expiry=True,
    ...         ),
    ...         spread_adjustment=ci.manage.SpreadAdjustment(
    ...             adjustment="arithmetic",
    ...             method=ci.SpreadAdjustmentMethod.CLOSE_TO_CLOSE,
    ...             backwards=True,
    ...         ),
    ...     ),
    ...
    >>> response_2 = create_udc(
    ...     symbol="MyUDCInstrument_DB",
    ...     instrument_name="ELBD Gbmx",
    ...     udc=ci.manage.UDC(
    ...         root="CC",
    ...         months=ci.manage.Months(
    ...             number_of_years=3,
    ...             include_all_months=True,
    ...             start_month=1,
    ...         ),
    ...         rollover=ci.manage.DayBasedRollover(
    ...             method=ci.DayBasedRolloverMethod.DAYS_BEFORE_END_OF_MONTH,
    ...             number_of_days=3,
    ...             months_prior=1,
    ...         ),
    ...         spread_adjustment=ci.manage.SpreadAdjustment(
    ...             adjustment="arithmetic",
    ...             method=ci.SpreadAdjustmentMethod.CLOSE_TO_CLOSE,
    ...             backwards=True,
    ...         ),
    ...     ),
    ...
    >>> response_3 = create_udc(
    ...     symbol="MyUDCInstrument_Manual",
    ...     instrument_name="REPKO Sys",
    ...     udc=ci.manage.UDC(
    ...         root="CC",
    ...         rollover=ci.manage.ManualRollover(
    ...             ci.manage.ManualItem(month=7, year=2021, start_date="2021-03-01"),
    ...             ci.manage.ManualItem(month=3, year=2020, start_date="2019-06-01"),
    ...         ),
    ...         spread_adjustment=ci.manage.SpreadAdjustment(
    ...             adjustment="arithmetic",
    ...             method=ci.SpreadAdjustmentMethod.CLOSE_TO_CLOSE,
    ...             backwards=True,
    ...         ),
    ...     ),
    """
    data = _create(
        symbol=symbol,
        type_=CustomInstrumentTypes.UDC,
        udc=udc,
        currency=currency,
        instrument_name=instrument_name,
        exchange_name=exchange_name,
        holidays=holidays,
        time_zone=time_zone,
        description=description,
        extended_params=extended_params,
        session=session,
        on_response=on_response,
    )
    return CustomInstrumentUDC(data, session=session)
