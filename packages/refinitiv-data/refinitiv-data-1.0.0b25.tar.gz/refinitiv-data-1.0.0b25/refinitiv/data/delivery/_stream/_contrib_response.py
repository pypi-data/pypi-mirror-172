class ContribResponse:
    def __init__(self, raw_response):
        self._raw_response = raw_response
        self._type = raw_response.get("Type")
        self._ack_id = raw_response.get("AckID")
        self._nak_code = raw_response.get("NakCode")
        self._text = raw_response.get("Text")
        self._debug = raw_response.get("Debug")

    def __repr__(self) -> str:  # noqa: D105
        rep = {"Type": self.type}
        if self.type == "Error":
            rep["Text"] = self.nak_message
            rep["Debug"] = self.debug
        else:
            rep["AckId"] = self.ack_id
            if self.nak_code:
                rep["NakCode"] = self.nak_code
                rep["Message"] = self.nak_message
        rep = str(rep)
        return rep

    @property
    def is_success(self) -> bool:
        return self.type == "Ack" and not self.nak_code

    @property
    def type(self) -> str:
        return self._type

    @property
    def ack_id(self) -> str:
        return self._ack_id

    @property
    def nak_code(self) -> str:
        return self._nak_code

    @property
    def nak_message(self) -> str:
        return self._text if self._type == "Ack" else ""

    @property
    def error(self):
        return self._text if self._type == "Error" else ""

    @property
    def debug(self) -> dict:
        return self._debug
