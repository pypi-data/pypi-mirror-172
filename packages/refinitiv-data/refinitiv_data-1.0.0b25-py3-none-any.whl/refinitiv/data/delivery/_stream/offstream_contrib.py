# coding: utf8

from typing import Any, Callable, TYPE_CHECKING

from ._offstream_contrib import _OffStreamContrib
from ._contrib_response import ContribResponse
from ._stream_factory import create_offstream_contrib
from .base_stream import StreamOpenWithUpdatesMixin
from ..._core.session import get_valid_session
from ..._tools import cached_property, create_repr, make_callback
from ...content._content_type import ContentType

if TYPE_CHECKING:
    from ... import OpenState
    from ...content._types import OptStr
    from ..._core.session import Session


class OffStreamContrib(StreamOpenWithUpdatesMixin):
    """
    OffStreamContrib client.

    Parameters
    ----------
    session: Session
        The Session defines the source where you want to retrieve your data
    name: string
        RIC to contribute on.
    api: string, optional
        specific name of OMM streaming defined in config file.
        i.e. 'streaming.contrib.endpoints.my_server'
        Default: 'streaming.contrib.endpoints.main'
    domain: string
        Specify item stream domain (MarketPrice, MarketByPrice, ...)
         (currently, offstream contribution accept only "MarketPrice")
        Default : "MarketPrice"
    service: string, optional
        Specify the service to contribute on.
        Default: None

    Raises
    ------
    Exception
        If request fails or if Refinitiv Services return an error

    Examples
    --------
    Prerequisite: The contrib session must be opened and set as default cnx
    >>> from refinitiv.data.delivery._stream.offstream_contrib import OffStreamContrib
    >>>
    >>> def on_ack_callback(ack_msg, stream):
    >>>     print("Receive Ack response:", ack_msg)
    >>>
    >>> contrib_offstream = OffStreamContrib(name="EUR", service="CONTRIB_FEED")
    >>> contrib_offstream.on_ack(on_ack_callback)
    >>> contrib_offstream.open()
    >>> update = {
    ...     "ASK": 1.23,
    ...     "BID": 1.24
    ... }
    >>> response = contrib_offstream.contribute(update)
    """

    def __init__(
        self,
        session: "Session",
        name: str,
        api: "OptStr" = None,
        domain: str = "MarketPrice",
        service: "OptStr" = None,
    ) -> None:
        self._session = get_valid_session(session)
        self._name = name
        self._api = api
        self._domain = domain
        self._service = service

    @cached_property
    def _stream(self) -> _OffStreamContrib:
        return create_offstream_contrib(
            ContentType.STREAMING_CONTRIB,
            session=self._session,
            name=self._name,
            api=self._api,
            domain=self._domain,
            service=self._service,
        )

    def open(self, with_updates: bool = True) -> "OpenState":
        """
        Opens the OMMStream to start to stream.
        Once it's opened, it can be used in order to retrieve data.

        Parameters
        ----------
        with_updates : bool, optional
            actions:
                True - the streaming will work as usual
                        and the data will be received continuously.
                False - only one data snapshot will be received
                        (single Refresh 'NonStreaming') and
                        stream will be closed automatically.

            Defaults to True

        Returns
        -------
        OpenState
            current state of this OMM stream object.

        Examples
        --------
        Prerequisite: The contrib session must be opened and set as default cnx
        >>> from refinitiv.data.delivery._stream.offstream_contrib import OffStreamContrib  # noqa
        >>>
        >>> def on_ack_callback(ack_msg, stream):
        >>>     print("Receive Ack response:", ack_msg)
        >>>
        >>> stream = OffStreamContrib(name="EUR", service="CONTRIB_FEED")
        >>> stream.on_ack(on_ack_callback)
        >>> stream.open()
        """
        self._stream.open(with_updates=with_updates)
        return self.open_state

    async def open_async(self, with_updates: bool = True) -> "OpenState":
        """
        Opens asynchronously the OffStreamContrib to start to contribute

        Returns
        -------
        OpenState
            current state of this OffStreamContrib object.

        Examples
        --------
        Prerequisite: The contrib session must be opened and set as default cnx
        >>> from refinitiv.data.delivery._stream.offstream_contrib import OffStreamContrib  # noqa
        >>>
        >>> def on_ack_callback(ack_msg, stream):
        >>>     print("Receive Ack response:", ack_msg)
        >>>
        >>> stream = OffStreamContrib(name="EUR", service="CONTRIB_FEED")
        >>> stream.on_ack(on_ack_callback)
        >>> await stream.open_async()
        """
        await self._stream.open_async(with_updates=False)
        return self.open_state

    def on_error(
        self, func: Callable[[dict, "OffStreamContrib"], Any]
    ) -> "OffStreamContrib":
        """
        This function called when an error occurs

        Parameters
        ----------
        func : Callable, optional
            Callable object to process when retrieved error data.

        Returns
        -------
        OffStreamContrib
            current instance of OffStreamContrib object.

        Examples
        --------
        Prerequisite: The contrib session must be opened and set as default cnx
        >>> from refinitiv.data.delivery._stream.offstream_contrib import OffStreamContrib  # noqa
        >>>
        >>> def on_ack_callback(ack_msg, stream):
        ...     print("Receive Ack response:", ack_msg)
        >>> def on_error_callback(error_msg, stream):
        ...     print("Receive Error:", error_msg)
        >>>
        >>> stream = OffStreamContrib(name="EUR", service="CONTRIB_FEED")
        >>> stream.on_ack(on_ack_callback)
        >>> stream.on_error(on_error_callback)
        >>> stream.open()
        >>> update = {
        ...     "ASK": "wrong value",
        ...     "BID": 1.24
        ... }
        >>> response = stream.contribute(update)
        """
        self._stream.on_error(make_callback(func))
        return self

    def on_ack(
        self, func: Callable[[dict, "OffStreamContrib"], Any]
    ) -> "OffStreamContrib":
        """
        This function called when the stream received an ack/nack message after sending an off stream contribution .

        Parameters
        ----------
        func : Callable, optional
             Callable object to process retrieved ack data

        Returns
        -------
        OffStreamContrib
            current instance of off stream contrib object.

        Examples
        --------
        Prerequisite: The contrib session must be opened and set as default cnx
        >>> from refinitiv.data.delivery._stream.offstream_contrib import OffStreamContrib  # noqa
        >>>
        >>> def on_ack_callback(ack_msg, stream):
        ...     print("Receive Ack response:", ack_msg)
        >>> def on_error_callback(error_msg, stream):
        ...     print("Receive Error:", error_msg)
        >>>
        >>> stream = OffStreamContrib(name="EUR", service="CONTRIB_FEED")
        >>> stream.on_ack(on_ack_callback)
        >>> stream.on_error(on_error_callback)
        >>> stream.open()
        >>> update = {
        ...     "ASK": 1.23,
        ...     "BID": 1.24
        ... }
        >>> response = stream.contribute(update)
        """
        self._stream.on_ack(make_callback(func))
        return self

    def __repr__(self):
        return create_repr(
            self,
            middle_path="offstream_contrib",
            class_name=self.__class__.__name__,
        )

    def contribute(
        self,
        fields_values: dict,
    ) -> "ContribResponse":
        """
        This function send the fields_values dict as an offstream contribution update.

        Parameters
        ----------
        fields_values: dict{field:value}
            Specify fields and values to contribute.

        Returns
        -------
        ContribResponse

        Examples
        --------
        Prerequisite: The contrib session must be opened and set as default cnx
        >>> from refinitiv.data.delivery._stream.offstream_contrib import OffStreamContrib  # noqa
        >>>
        >>> def on_ack_callback(ack_msg, stream):
        ...     print("Receive Ack response:", ack_msg)
        >>> def on_error_callback(error_msg, stream):
        ...     print("Receive Error:", error_msg)
        >>>
        >>> contrib_stream = OffStreamContrib(name="EUR", service="CONTRIB_FEED")
        >>> contrib_stream.on_ack(on_ack_callback)
        >>> contrib_stream.on_error(on_error_callback)
        >>> contrib_stream.open()
        >>> update = {
        ...     "ASK": "wrong value",
        ...     "BID": 1.24
        ... }
        >>> response = contrib_stream.contribute(update)
        """
        return self._stream.contribute(fields_values)

    async def contribute_async(
        self,
        fields_values: dict,
    ) -> "ContribResponse":
        """
        This function send asynchronously the fields_values dict as an offstream contribution update.

        Parameters
        ----------
        fields_values: dict{field:value}
            Specify fields and values to contribute.

        Returns
        -------
        ContribResponse

        Examples
        --------
        Prerequisite: The contrib session must be opened and set as default cnx
        >>> from refinitiv.data.delivery._stream.offstream_contrib import OffStreamContrib  # noqa
        >>>
        >>> def on_ack_callback(ack_msg, stream):
        ...     print("Receive Ack response:", ack_msg)
        >>> def on_error_callback(error_msg, stream):
        ...     print("Receive Error:", error_msg)
        >>>
        >>> contrib_stream = OffStreamContrib(name="EUR", service="CONTRIB_FEED")
        >>> contrib_stream.on_ack(on_ack_callback)
        >>> contrib_stream.on_error(on_error_callback)
        >>> contrib_stream.open()
        >>> update = {
        ...     "ASK": "wrong value",
        ...     "BID": 1.24
        ... }
        >>> response = await contrib_stream.contribute_async(update)
        """
        return await self._stream.contribute_async(fields_values)
