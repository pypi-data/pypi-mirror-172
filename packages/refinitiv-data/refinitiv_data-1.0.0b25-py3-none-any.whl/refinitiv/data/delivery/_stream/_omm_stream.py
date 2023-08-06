# coding: utf-8
import os
import socket
from typing import Callable, Optional, TYPE_CHECKING, Any

from ._protocol_type import ProtocolType
from ._stream_contrib_mixin import OMMContribMixin
from ._stream_listener import OMMStreamListener, StreamEvent
from .stream import (
    Stream,
    update_message_with_extended_params,
)
from ..._tools import cached_property
from ...content._types import OptStr, ExtendedParams, Strings

if TYPE_CHECKING:
    from ._stream_factory import StreamDetails
    from . import StreamConnection
    from ..._core.session import Session
    from ._contrib_response import ContribResponse


class _OMMStream(Stream, OMMStreamListener["_OMMStream"], OMMContribMixin):
    _message = None
    _code = None
    _with_updates: bool = True

    def __init__(
        self,
        stream_id: int,
        session: "Session",
        name: str,
        details: "StreamDetails",
        domain: OptStr = "MarketPrice",
        service: OptStr = None,
        fields: Optional[Strings] = None,
        key: Optional[dict] = None,
        extended_params: ExtendedParams = None,
        on_refresh: Optional[Callable] = None,
        on_status: Optional[Callable] = None,
        on_update: Optional[Callable] = None,
        on_complete: Optional[Callable] = None,
        on_error: Optional[Callable] = None,
        on_ack: Optional[Callable] = None,
    ) -> None:
        Stream.__init__(self, stream_id, session, details)
        OMMStreamListener.__init__(
            self,
            logger=session.logger(),
            on_refresh=on_refresh,
            on_status=on_status,
            on_update=on_update,
            on_complete=on_complete,
            on_error=on_error,
            on_ack=on_ack,
        )
        OMMContribMixin.__init__(self)
        self._name = name
        self._service = service
        self._fields = fields or []
        self._domain = domain
        self._key = key
        self._extended_params = extended_params
        self._post_id = None
        self._post_user_info = None

    @property
    def post_id(self) -> int:
        return self._post_id

    @property
    def post_user_info(self) -> dict:
        return self._post_user_info

    @property
    def name(self) -> str:
        return self._name

    @property
    def protocol_type(self) -> ProtocolType:
        return ProtocolType.OMM

    @property
    def code(self):
        return self._code

    @property
    def message(self):
        return self._message

    @property
    def open_message(self):
        msg = {
            "ID": self.id,
            "Domain": self._domain,
            "Streaming": self._with_updates,
            "Key": {},
        }

        if self._key:
            msg["Key"] = self._key

        msg["Key"]["Name"] = self.name

        if self._service:
            msg["Key"]["Service"] = self._service

        if self._fields:
            msg["View"] = self._fields

        if self._extended_params:
            msg = update_message_with_extended_params(msg, self._extended_params)

        return msg

    @cached_property
    def close_message(self):
        return {"ID": self.id, "Type": "Close"}

    def get_contrib_message(self, fields_values: dict, contrib_type: str) -> dict:
        message = {
            "Ack": True,
            "ID": self.id,
            "Message": {
                "Fields": fields_values,
                "ID": 0,
                "Type": contrib_type,
                "Domain": self._domain,
            },
            "PostID": self._post_id,
            "Type": "Post",
            "Domain": self._domain,
        }

        post_user_info = self._post_user_info
        if not post_user_info:
            hostname = socket.gethostname()
            ip_addr = socket.gethostbyname(hostname)
            post_user_info = {"Address": ip_addr, "UserID": os.getpid()}

        message["PostUserInfo"] = post_user_info

        return message

    def contribute(
        self,
        fields_values: dict,
        contrib_type: str = "Update",
        post_user_info: Optional[dict] = None,
    ) -> "ContribResponse":
        self._post_id = next(self.session._contrib_post_id_counter)
        self._post_user_info = post_user_info
        return super().contribute(fields_values, contrib_type)

    async def contribute_async(
        self,
        fields_values: dict,
        contrib_type: str = "Update",
        post_user_info: Optional[dict] = None,
    ) -> "ContribResponse":
        self._post_id = next(self.session._contrib_post_id_counter)
        self._post_user_info = post_user_info
        return await super().contribute_async(fields_values, contrib_type)

    def _do_open(self, *args, **kwargs):
        self._with_updates = kwargs.get("with_updates", True)
        self._initialize_cxn()
        self._cxn.on(self._event.refresh_by_id, self._on_stream_refresh)
        self._cxn.on(self._event.update_by_id, self._on_stream_update)
        self._cxn.on(self._event.status_by_id, self._on_stream_status)
        self._cxn.on(self._event.complete_by_id, self._on_stream_complete)
        self._cxn.on(self._event.error_by_id, self._on_stream_error)
        super()._do_open(*args, **kwargs)

    def _dispose(self):
        self._debug(f"{self._classname} disposing [d]")
        self._cxn.remove_listener(self._event.refresh_by_id, self._on_stream_refresh)
        self._cxn.remove_listener(self._event.update_by_id, self._on_stream_update)
        self._cxn.remove_listener(self._event.status_by_id, self._on_stream_status)
        self._cxn.remove_listener(self._event.complete_by_id, self._on_stream_complete)
        self._cxn.remove_listener(self._event.error_by_id, self._on_stream_error)
        self._release_cxn()
        self._debug(f"{self._classname} disposed [D]")

    def _do_on_stream_refresh(self, cxn: "StreamConnection", message, *args) -> Any:
        message_state = message.get("State", {})
        self._code = message_state.get("Stream", "")
        self._message = message_state.get("Text", "")
        return message

    def _on_stream_status(self, originator, *args) -> None:
        self._propagate_event(StreamEvent.STATUS, originator, *args)

        if self.is_open:
            self.dispatch_complete(originator, *args)

    def _do_on_stream_status(self, cxn: "StreamConnection", message: dict, *_) -> Any:
        message_state = message.get("State", {})
        stream_state = message_state.get("Stream", "")

        self._code = stream_state
        self._message = message_state.get("Text", "")

        if stream_state == "Closed":
            self._debug(
                f"{self._classname} received a closing message, "
                f"message_state={message_state}, state={self.state}"
            )

            if self.is_opening:
                self._opened.set()

        return message

    def _do_on_stream_ack(self, originator: "StreamConnection", *args) -> Any:
        return super()._do_on_stream_ack(originator, *args)

    def _do_on_stream_error(self, originator, *args) -> Any:
        return super()._do_on_stream_error(originator, *args)

    def send_open_message(self):
        self.send(self.open_message)

    def _on_stream_complete(self, originator, *args) -> None:
        self._propagate_event(StreamEvent.COMPLETE, originator, *args)

        if self.is_opening:
            self._opened.set()
