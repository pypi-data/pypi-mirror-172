from typing import Union, List, Dict

from ._context import RDPMixin
from ._hp_context import HPContext


class HPRDPContext(RDPMixin, HPContext):
    def prepare_headers(self, raw: Union[list, dict], *args) -> List[Dict]:
        headers = [
            {"name": "instrument", "title": "Instrument"},
            {"name": "date", "title": "Date"},
        ]

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

            headers.append({"name": name, "title": name})

        return headers
