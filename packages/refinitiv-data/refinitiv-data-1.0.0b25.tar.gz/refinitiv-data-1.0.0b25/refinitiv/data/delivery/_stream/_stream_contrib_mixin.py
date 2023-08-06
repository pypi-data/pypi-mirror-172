# coding: utf8
import asyncio
import json
from functools import partial
from threading import Event
from typing import TYPE_CHECKING, Any, Optional, Callable

from ._contrib_response import ContribResponse

if TYPE_CHECKING:
    from . import StreamConnection, StreamState


class OMMContribMixin:
    post_id: int
    get_contrib_message: Callable[[dict, str], dict]
    send: Callable[[dict], bool]
    _error: Callable[[Any], None]
    _debug: Callable[[Any], None]
    _classname: str
    state: "StreamState"

    def __init__(self):
        self._contributed = Event()
        self._message: Optional[dict] = None
        self._is_contributing = False

    @property
    def is_contributing(self):
        return self._is_contributing

    def contribute(
        self, fields_values: dict, contrib_type: str = "Update"
    ) -> ContribResponse:
        self._contributed.clear()
        self._is_contributing = True

        sent = self.send(self.get_contrib_message(fields_values, contrib_type))
        if sent:
            self._contributed.wait()
            self._is_contributing = False
            response = ContribResponse(self._message)

        else:
            response = ContribResponse({})

        return response

    async def contribute_async(
        self, fields_values: dict, contrib_type: str = "Update"
    ) -> ContribResponse:
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(
            None, partial(self.contribute, fields_values, contrib_type)
        )

    def _do_on_stream_ack(
        self, originator: "StreamConnection", message: dict, *args
    ) -> Any:
        self._message = message
        ack_id = message.get("AckID")
        nack_code = message.get("NakCode")

        if ack_id != self.post_id:
            # Received Ack message with wrong ack_id
            self._error(
                f"{self._classname} Received Ack message "
                f"with wrong ack_id={ack_id} != post_id={self.post_id}"
            )
        else:
            if nack_code:
                reason = message.get("Text")
                self._error(
                    f"{self._classname} received Nack message, "
                    f"ackID={ack_id}, NackCode={nack_code}, reason={reason}"
                )

            else:
                self._debug(
                    f"{self._classname} received Ack message, "
                    f"ackID={ack_id}, state={self.state}"
                )

            self._contributed.set()

        return message

    def _do_on_stream_error(
        self, originator: "StreamConnection", message: dict, *args
    ) -> Any:
        if message.get("Type") == "Error":
            debug_message = message.get("Debug", {}).get("Message")
            if debug_message:
                try:
                    debug_dict = json.loads(debug_message)
                    if debug_dict.get("PostID"):
                        self._message = message
                except json.decoder.JSONDecodeError:
                    self._error(f"Cannot decode Debug message as JSON: {debug_message}")

        if self.is_contributing:
            self._contributed.set()

        return message
