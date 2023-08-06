from typing import TYPE_CHECKING

from .._stream.offstream_contrib import OffStreamContrib

if TYPE_CHECKING:
    from ..._core.session import Session
    from .._stream._contrib_response import ContribResponse
    from ...content._types import OptStr, OptCall


def contribute(
    name: str,
    fields_values: dict,
    *,
    service: "OptStr" = None,
    session: "Session" = None,
    api: "OptStr" = None,
    on_ack: "OptCall" = None,
    on_error: "OptCall" = None,
) -> "ContribResponse":
    """
    Function to send OffStream contribution request.

    Parameters
    ----------
    name: string
        RIC to retrieve item stream.

    fields_values: dict{field:value}
        Specify fields and values to contribute.

    service: string, optional
        Specify the service to contribute on.
        Default: None

    session: Session, optional
        Specify the session used to contribute

    api: string, optional
        specific name of contrib streaming defined in config file.
        i.e. 'streaming.contrib.endpoints.my_server'
        Default: 'streaming.contrib.endpoints.main'

    on_ack : function, optional
        Callback function for on_ack event to check contribution result

    on_error : function, optional
        Callback function for on_error event

    Returns
    ----------
    ContribResponse

    Examples
    --------
    Prerequisite: The contrib_session must be opened
    >>> import refinitiv.data as rd
    >>> def on_ack_callback(ack_msg, stream):
    ...     print("Receive Ack response:", ack_msg)
    >>> def on_error_callback(error_msg, stream):
    ...     print("Receive Error:", error_msg)
    >>> update = {
    ...     "ASK": 1.23,
    ...     "BID": 1.24
    ... }
    >>> response = rd.delivery.omm_stream.contribute(
    ...     name="EUR=",
    ...     fields_values=update,
    ...     service="SVC_CONTRIB",
    ...     on_ack=on_ack_callback,
    ...     on_error=on_error_callback
    ... )
    """
    offstream = OffStreamContrib(
        session=session,
        name=name,
        service=service,
        api=api,
    )
    on_ack and offstream.on_ack(on_ack)
    on_error and offstream.on_error(on_error)
    offstream.open()
    return offstream.contribute(fields_values)


async def contribute_async(
    name: str,
    fields_values: dict,
    *,
    service: "OptStr" = None,
    session: "Session" = None,
    api: "OptStr" = None,
    on_ack: "OptCall" = None,
    on_error: "OptCall" = None,
) -> "ContribResponse":
    """
    Function to send asynchrnous OffStream contribution request.

    Parameters
    ----------
    name: string
        RIC to retrieve item stream.

    fields_values: dict{field:value}
        Specify fields and values to contribute.

    service: string, optional
        Specify the service to contribute on.
        Default: None

    session: Session, optional
        Specify the session used to contribute

    api: string, optional
        specific name of contrib streaming defined in config file.
        i.e. 'streaming.contrib.endpoints.my_server'
        Default: 'streaming.contrib.endpoints.main'

    on_ack : function, optional
        Callback function for on_ack event to check contribution result

    on_error : function, optional
        Callback function for on_error event

    Returns
    ----------
    ContribResponse

    Examples
    --------
    Prerequisite: The contrib_session must be opened.
    >>> import refinitiv.data as rd
    >>> def on_ack_callback(ack_msg, stream):
    ...     print("Receive Ack response:", ack_msg)
    >>> def on_error_callback(error_msg, stream):
    ...     print("Receive Error:", error_msg)
    >>> update = {
    ...     "ASK": 1.23,
    ...     "BID": 1.24
    ... }
    >>> response = await rd.delivery.omm_stream.contribute_async(
    ...     "EUR=",
    ...     fields_values=update,
    ...     service="SVC_CONTRIB",
    ...     on_ack=on_ack_callback,
    ...     on_error=on_error_callback
    ... )
    """
    offstream = OffStreamContrib(
        session=session,
        service=service,
        name=name,
        api=api,
    )
    on_ack and offstream.on_ack(on_ack)
    on_error and offstream.on_error(on_error)
    await offstream.open_async()
    return await offstream.contribute_async(fields_values)
