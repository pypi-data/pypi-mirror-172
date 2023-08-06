import abc
from typing import Optional, Dict, Tuple, List, Callable

from pandas import DataFrame

from ._context import Context
from .. import working_with_missing_data_and_convert_dtypes
from .._containers import FieldsContainer
from .._intervals_consts import NON_INTRA_DAY_INTERVALS
from ..._tools import ohlc
from ...content._historical_df_builder import process_historical_raw
from ...content._types import StrStrings


class HPContext(Context, abc.ABC):
    @property
    def can_get_data(self) -> bool:
        return bool(self.universe.hp and (not self.fields or self.fields.hp))

    @property
    def is_no_fields(self) -> bool:
        return bool(self.fields.is_no_hp and self.fields.adc == ["TR.RIC"])

    @property
    def can_build_df(self) -> bool:
        return bool(self._hp_data and not (self._adc_data or self._cust_inst_data))

    @property
    def raw(self) -> Optional[Dict]:
        return self._hp_data and self._hp_data.raw

    @property
    def df(self) -> Optional[DataFrame]:
        return self._hp_data and self._hp_data.df

    def build_df(self, *args) -> DataFrame:
        df = working_with_missing_data_and_convert_dtypes(self.df)
        df.ohlc = ohlc.__get__(df, None)
        return df

    def prepare_to_build(self, interval, *args):
        data, fields = self.prepare_data(interval)
        self._data = data

        if self.is_no_fields:
            if not isinstance(fields, FieldsContainer):
                fields = FieldsContainer(fields)

            self.fields = fields

        self._headers = self.prepare_headers(self.raw)

    def prepare_data(self, interval: str, *args):
        """
        Transform historical pricing data to further merging.

        Transformed data looks like:
        {
            "RIC": [{"Date": "value", "field": "value", "another_field": "value"}],
            "NEXT_RIC": [{"Date": "value", "field": "value", "next_field": "value"}]
        }
        """
        if interval in NON_INTRA_DAY_INTERVALS:

            def parse_date_value(dt):
                return str(dt).split(" ")[0]

        else:

            def parse_date_value(dt):
                return str(dt)

        if isinstance(self.raw, dict):
            return self._parse_dict_to_data_fields(parse_date_value)

        elif isinstance(self.raw, list):
            return self._parse_list_to_data_fields(parse_date_value)

    def _parse_list_to_data_fields(
        self, parse_date_value: Callable
    ) -> Tuple[List[List[dict]], StrStrings]:
        data = [[] for _ in self.universe.hp]
        fields = self.fields.hp

        for index, item in enumerate(self.raw):
            if isinstance(item, list):
                data[index].append({"Type": "pricing", self.date_name: None})

            else:
                if not fields:
                    fields = [header["name"] for header in item["headers"]]

                raw_datas, _, raw_dates = process_historical_raw(item, fields)
                for raw_data, raw_date in zip(raw_datas, raw_dates):
                    item = {
                        "Type": "pricing",
                        self.date_name: parse_date_value(raw_date),
                    }
                    item.update((item for item in zip(fields, raw_data)))
                    data[index].append(item)

        return data, fields

    def _parse_dict_to_data_fields(
        self, parse_date_value: Callable
    ) -> Tuple[List[List[dict]], StrStrings]:
        fields = self.fields.hp
        data = []

        raw_datas, raw_columns, raw_dates = process_historical_raw(self.raw, fields)

        for raw_data, raw_date in zip(raw_datas, raw_dates):
            item = {
                "Type": "pricing",
                self.date_name: parse_date_value(raw_date),
            }

            if fields:
                item.update((item for item in zip(fields, raw_data)))

            else:
                item.update((item for item in zip(raw_columns, raw_data)))

            data.append(item)

        if not fields:
            fields = raw_columns

        lists = [[] for _ in self.universe.hp]
        lists[0] = data
        return lists, fields
