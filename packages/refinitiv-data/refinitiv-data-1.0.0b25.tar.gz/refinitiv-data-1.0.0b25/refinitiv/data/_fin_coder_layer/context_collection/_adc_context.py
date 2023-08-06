import abc
from collections import Counter
from itertools import groupby
from typing import Optional, Dict, List

from pandas import DataFrame

from ._context import Context
from .._containers import UniverseContainer
from .._history_provider import group_universe, chunks
from .._intervals_consts import NON_INTRA_DAY_INTERVALS
from .._tools import working_with_missing_data_and_convert_dtypes
from ..._tools import ohlc


class ADCContext(Context, abc.ABC):
    @property
    def can_build_df(self) -> bool:
        return bool(self._adc_data and not (self._hp_data or self._cust_inst_data))

    @property
    def can_get_data(self) -> bool:
        return bool(self.universe.adc)

    @property
    def raw(self) -> Optional[Dict]:
        return self._adc_data and self._adc_data.raw

    @property
    def df(self) -> Optional[DataFrame]:
        return self._adc_data and self._adc_data.df

    @abc.abstractmethod
    def is_raw_headers_in_fields(self, raw, fields) -> bool:
        # for override
        pass

    def build_df(self, *args) -> DataFrame:
        df = self.df
        if not self.is_raw_headers_in_fields(self.raw, self.fields):
            df = DataFrame()

        df.sort_index(ascending=True, inplace=True)
        df = working_with_missing_data_and_convert_dtypes(df)
        df.ohlc = ohlc.__get__(df, None)
        return df

    @abc.abstractmethod
    def get_cols(self, headers, fields, *args) -> List[str]:
        # for override
        pass

    def prepare_data(self, interval, *args):
        """
        Transform adc data to further merging.

        Transformed data looks like:
        {
            "RIC": [{"Date": "value", "field": "value", "another_field": "value"}],
            "NEXT_RIC": [{"Date": "value", "field": "value", "next_field": "value"}]
        }
        """
        headers = self.dfbuilder.get_headers(self.raw)
        cols = ["Type", *self.get_cols(headers, self.fields.adc)]
        data = []
        universe = []
        index_universe = 0
        universe_count = group_universe(self.universe.adc)
        len_universe_count = len(universe_count)
        counter_items = Counter()

        if interval in NON_INTRA_DAY_INTERVALS:

            def process_item_date(s: str) -> str:
                return s.split("T")[0]

        else:

            def process_item_date(s: str) -> str:
                return s.replace("T", " ").replace("Z", "")

        for ric, items in groupby(self.raw["data"], lambda i: i[0]):
            items = list(items)
            len_items = len(items)
            counter_items.update([len_items])
            result_items = []

            if index_universe < len_universe_count:
                name_universe, count = universe_count[index_universe]

            else:
                count = 0
                name_universe = ""

            for item in items:
                item[0] = "adc"
                item = {k: v for k, v in zip(cols, item)}
                item_date = item.get(self.date_name)

                if item_date:
                    item[self.date_name] = process_item_date(item_date)

                result_items.append(item)

            repeat_universe = 1
            if ric == name_universe:

                if count == len_items:
                    repeat_universe = count

                    for i in result_items:
                        data.append([i])

                elif (
                    count < len_items
                    and counter_items.most_common(1)[0][0] * (count + 1) == len_items
                ):
                    repeat_universe = count + 1
                    for chunk in chunks(result_items, len_items // repeat_universe):
                        data.append(chunk)

                elif count < len_items:
                    repeat_universe = count
                    for chunk in chunks(result_items, len_items // count):
                        data.append(chunk)

                elif count > len_items:
                    for chunk in chunks(result_items, len_items):
                        data.append(chunk)

                index_universe += 1

            else:
                data.append(result_items)

            universe.extend([ric] * repeat_universe)

        return data, universe

    def prepare_to_build(self, interval, *args):
        data, universe = self.prepare_data(interval)
        self.universe = UniverseContainer(universe)
        self._data = data
        self._headers = self.prepare_headers(self.raw)
