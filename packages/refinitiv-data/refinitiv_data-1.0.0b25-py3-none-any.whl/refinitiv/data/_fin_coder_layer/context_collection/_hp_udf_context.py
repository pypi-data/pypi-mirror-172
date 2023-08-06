from typing import Union, List, Dict

from ._context import UDFMixin
from ._hp_context import HPContext


class HPUDFContext(UDFMixin, HPContext):
    def prepare_headers(self, raw: Union[list, dict], *args) -> List[List[Dict]]:
        headers = [{"displayName": "Instrument"}, {"displayName": "Date"}]

        if isinstance(raw, list):
            raw = raw[0]["headers"]

        elif isinstance(raw, dict):
            raw = raw["headers"]

        else:
            raw = []

        for item in raw:
            name = item["name"]

            if name.lower() in {"date", "instrument"}:
                continue

            headers.append({"displayName": name, "field": name})

        return [headers]
