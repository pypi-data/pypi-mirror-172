from typing import List

from ._adc_context import ADCContext
from ._context import UDFMixin


class ADCUDFContext(UDFMixin, ADCContext):
    def prepare_headers(self, raw: dict, *args) -> List[List[str]]:
        """
        Prepare headers to pass them to df_builder.

        Args:
            raw (dict): adc raw data from adc response.

        Returns:
            List with inserted list of dicts that describe each header in understandable
            by df builder format.
        """
        fields = self.fields.raw

        field_to_idx = {field.upper(): fields.index(field) + 2 for field in fields}
        headers = [{"displayName": "Instrument"}, {"displayName": "Date"}]

        for header in raw["headers"][0]:
            if len(header) > 1:
                field_upper = header["field"].upper()

                if field_upper not in field_to_idx:
                    continue

                headers.insert(field_to_idx[field_upper], header)
                field_to_idx.pop(field_upper)

        for field, index in field_to_idx.items():
            headers.insert(index, {"displayName": field, "field": field})

        return [headers]

    def get_cols(self, headers, *args) -> List[str]:
        return [col["name"] for col in headers if col["name"] != "Instrument"]

    def is_raw_headers_in_fields(self, raw, fields) -> bool:
        fields = {field.casefold() for field in fields}
        headers = set()

        for header in raw["headers"][0]:
            if header.get("field"):
                headers.add(header.get("field").casefold())

        return headers.issubset(fields)
