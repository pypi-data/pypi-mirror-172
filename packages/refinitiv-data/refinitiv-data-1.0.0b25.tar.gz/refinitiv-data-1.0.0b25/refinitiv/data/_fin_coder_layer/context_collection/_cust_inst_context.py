import abc
from typing import Dict, Optional

import pandas as pd
from pandas import DataFrame

from .. import working_with_missing_data_and_convert_dtypes
from ._context import Context
from ..._tools import ohlc


class CustInstContext(Context, abc.ABC):
    @property
    def can_get_data(self) -> bool:
        return bool(self.universe.cust_inst)

    @property
    def can_build_df(self) -> bool:
        return bool(self._cust_inst_data and not (self._adc_data or self._hp_data))

    @property
    def raw(self) -> Optional[Dict]:
        return self._cust_inst_data and self._cust_inst_data.raw

    @property
    def df(self) -> Optional[DataFrame]:
        return self._cust_inst_data and self._cust_inst_data.df

    def build_df(self, use_field_names_in_headers: bool, *args) -> DataFrame:
        fields = self.fields
        df = self.df
        if fields:
            data = self.prepare_data(self.raw, fields)
            headers = self.prepare_headers(fields.raw)
            df = self.dfbuilder.build_date_as_index(
                {"data": data, "headers": headers},
                use_field_names_in_headers,
                use_multiindex=len(fields.raw) > 1 and len(self.universe.cust_inst) > 1,
            )
        df = working_with_missing_data_and_convert_dtypes(df)
        df.ohlc = ohlc.__get__(df, None)
        return df

    def _get_fields_from_raw(self):
        fields = []
        if isinstance(self.raw, list):
            headers = self.raw[0]["headers"]

        else:
            headers = self.raw["headers"]

        for header in headers:
            name = header.get("name")
            if name and name.lower() not in {"date", "instrument"}:
                fields.append(name)

        return fields

    def _get_fields_from_headers(self, headers, use_field_names_in_headers):
        name = "name" if use_field_names_in_headers else "title"
        return [
            header[name]
            for header in self.dfbuilder.get_headers({"headers": headers})
            if header[name].lower() not in {"date", "instrument"}
        ]

    def prepare_to_build(
        self, use_field_names_in_headers, df: DataFrame, headers, *args
    ):
        if not self.fields:
            fields = self._get_fields_from_raw()

        else:
            fields = self._get_fields_from_headers(headers, use_field_names_in_headers)

        data = self.prepare_data(self.raw, fields)
        headers = self.prepare_headers(fields)
        other = self.dfbuilder.build_date_as_index(
            {"data": data, "headers": headers},
            use_field_names_in_headers,
            use_multiindex=True,
        )

        if (not self._adc_data and self._hp_data) or (
            self._adc_data and not self._hp_data
        ):
            df = df.join(other, how="outer")
        else:
            df = pd.merge(df, other, on=["Date"])

        self._cust_inst_data._df = df
