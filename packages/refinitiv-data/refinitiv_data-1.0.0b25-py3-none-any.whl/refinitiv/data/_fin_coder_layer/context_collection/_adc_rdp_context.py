from typing import List

from ._adc_context import ADCContext
from ._context import RDPMixin


class ADCRDPContext(RDPMixin, ADCContext):
    def prepare_headers(self, raw: dict, *args) -> List[List[str]]:
        fields = self.fields.raw
        field_to_idx = {field.casefold(): fields.index(field) + 2 for field in fields}

        headers = [
            {"name": "instrument", "title": "Instrument"},
            {"name": "date", "title": "Date"},
        ]

        for header in raw["headers"]:
            field = f"{header['name']}.{header['title']}".casefold()
            header_name = header["name"].casefold()

            if header_name in field_to_idx and field not in field_to_idx:
                headers.insert(field_to_idx[header_name], header)
                field_to_idx.pop(header_name)

            if field in field_to_idx:
                headers.insert(field_to_idx[field], header)
                field_to_idx.pop(field)

        for field, index in field_to_idx.items():
            headers.insert(index, {"name": field.upper(), "title": field.upper()})

        return headers

    def get_cols(self, headers, fields, *args) -> List[str]:
        cols = []
        fields = [field.casefold() for field in fields]

        for header in headers:
            header_name = header["name"]
            header_title = header["title"]
            field = f"{header_name}.{header_title}".casefold()

            if header_name.casefold() == "instrument":
                continue

            elif field in fields:
                cols.append(f"{header_name}.{header_title}")

            else:
                cols.append(header_name)

        return cols

    def is_raw_headers_in_fields(self, raw, fields) -> bool:
        fields = {field.casefold() for field in fields}
        headers = set()

        for header in raw["headers"]:
            header_name = header["name"]
            if header_name not in {"instrument", "date"} and ")" not in header_name:
                header_title = header["title"]

                if " " in header_title:
                    headers.add(header_name.casefold())

                elif header_name == "RIC" and header_title == "RIC":
                    headers.add("tr.ric")

                else:
                    if header_name.split(".")[-1] == header_title:
                        headers.add(header_name.casefold())

                    else:
                        headers.add(
                            f"{header_name.casefold()}.{header_title.casefold()}"
                        )

        return headers.issubset(fields)
