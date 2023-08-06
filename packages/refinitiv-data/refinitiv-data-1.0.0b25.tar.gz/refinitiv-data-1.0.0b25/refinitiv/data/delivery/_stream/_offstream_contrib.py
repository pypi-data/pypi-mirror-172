# coding: utf-8

from typing import Callable, Optional, TYPE_CHECKING, Any

from ._protocol_type import ProtocolType
from ._stream_listener import OMMStreamListener
from .stream import Stream
from .stream_connection import LOGIN_STREAM_ID
from ._stream_contrib_mixin import OMMContribMixin
from ..._tools import cached_property

if TYPE_CHECKING:
    from ._stream_factory import StreamDetails
    from . import StreamConnection
    from ..._core.session import Session
    from ._contrib_response import ContribResponse


class _OffStreamContrib(
    Stream, OMMStreamListener["_OffStreamContrib"], OMMContribMixin
):
    def __init__(
        self,
        post_id: int,
        session: "Session",
        name: str,
        details: "StreamDetails",
        service: str,
        domain: str,
        on_ack: Optional[Callable] = None,
        on_error: Optional[Callable] = None,
    ) -> None:
        Stream.__init__(self, post_id, session, details)
        OMMStreamListener.__init__(
            self,
            logger=session.logger(),
            on_ack=on_ack,
            on_error=on_error,
        )
        OMMContribMixin.__init__(self)
        self._name = name
        self._service = service
        self._domain = domain

    @property
    def name(self) -> str:
        return self._name

    @property
    def protocol_type(self) -> ProtocolType:
        return ProtocolType.OMM

    @property
    def post_id(self) -> int:
        return self.id

    @cached_property
    def post_by_id(self) -> str:
        return self._event.ack_by_id

    @cached_property
    def error_by_id(self) -> str:
        return self._event.error_by_id

    def get_contrib_message(self, fields_values: dict, contrib_type: str) -> dict:
        return {
            "Ack": True,
            "ID": LOGIN_STREAM_ID,
            "Message": {
                "Fields": fields_values,
                "ID": 0,
                "Type": contrib_type,
                "Domain": self._domain,
            },
            "PostID": self.post_id,
            "Type": "Post",
            "Key": {"Name": self._name, "Service": self._service},
            "Domain": self._domain,
        }

    def _do_open(self, *args, **kwargs):
        self._initialize_cxn()
        self._cxn.on(self._event.error_by_id, self._on_stream_error)

    def _do_close(self, *args, **kwargs):
        self._dispose()

    def _dispose(self):
        self._debug(f"{self._classname} disposing [d]")
        self._release_cxn()
        self._debug(f"{self._classname} disposed [D]")

    def contribute(
        self, fields_values: dict, contrib_type: str = "Update"
    ) -> "ContribResponse":
        self._debug(f"Listen Ack event for {self.post_by_id}")
        self._cxn.on(self.post_by_id, self._on_stream_ack)
        self._debug(f"Listen Error event for {self.error_by_id}")
        self._cxn.on(self.error_by_id, self._on_stream_error)
        return OMMContribMixin.contribute(self, fields_values)

    async def contribute_async(
        self, fields_values: dict, contrib_type: str = "Update"
    ) -> "ContribResponse":
        return await OMMContribMixin.contribute_async(self, fields_values)

    def _do_on_stream_ack(self, originator: "StreamConnection", *args) -> Any:
        self._cxn.remove_listener(self.post_by_id, self._on_stream_ack)
        return OMMContribMixin._do_on_stream_ack(self, originator, *args)

    def _do_on_stream_error(self, originator, *args) -> Any:
        return OMMContribMixin._do_on_stream_error(self, originator, *args)
