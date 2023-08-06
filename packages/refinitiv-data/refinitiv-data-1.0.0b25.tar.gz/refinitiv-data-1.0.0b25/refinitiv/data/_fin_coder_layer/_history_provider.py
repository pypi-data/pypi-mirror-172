import abc
from itertools import groupby, zip_longest
from typing import TYPE_CHECKING, List

from ._intervals_consts import NON_INTRA_DAY_INTERVALS
from .._fin_coder_layer._tools import working_with_missing_data_and_convert_dtypes
from .._tools import ohlc

if TYPE_CHECKING:
    from .context_collection import ADCContext, CustInstContext, HPContext
    from ._containers import FieldsContainer, UniverseContainer
    from ..content._df_builder import DFBuilder


class HistoryProvider(abc.ABC):
    @property
    @abc.abstractmethod
    def dfbuilder(self) -> "DFBuilder":
        #  for override
        pass

    @property
    @abc.abstractmethod
    def date_name(self) -> str:
        #  for override
        pass

    def get_df(
        self,
        adc: "ADCContext",
        hp: "HPContext",
        cust_inst: "CustInstContext",
        universe: "UniverseContainer",
        fields: "FieldsContainer",
        interval: str,
        use_field_names_in_headers: bool,
    ):
        if adc.can_build_df:
            return adc.build_df()

        if hp.can_build_df:
            return hp.build_df()

        if cust_inst.can_build_df:
            return cust_inst.build_df(use_field_names_in_headers)

        return self.build_common_df(
            adc, hp, cust_inst, universe, fields, interval, use_field_names_in_headers
        )

    def build_common_df(
        self,
        adc: "ADCContext",
        hp: "HPContext",
        cust_inst: "CustInstContext",
        universe: "UniverseContainer",
        fields: "FieldsContainer",
        interval: str,
        use_field_names_in_headers: bool,
    ):
        comm_universe = universe.hp
        headers = None
        if hp.raw:
            hp.prepare_to_build(interval)
            headers = hp.headers
            fields = hp.fields

        if adc.raw:
            adc.prepare_to_build(interval)
            comm_universe = adc.universe
            headers = adc.headers

        data = prepare_data(adc.data, hp.data, comm_universe, fields, self.date_name)
        df = self.dfbuilder.build_date_as_index(
            {"data": data, "headers": headers},
            use_field_names_in_headers,
            use_multiindex=bool(cust_inst.raw),
        )

        if cust_inst.raw:
            cust_inst.prepare_to_build(use_field_names_in_headers, df, headers)
            df = cust_inst.df

        df = working_with_missing_data_and_convert_dtypes(df)

        if len(comm_universe) > 1:
            df.rename(columns={k: v for k, v in enumerate(comm_universe)}, inplace=True)

        if interval is not None and interval not in NON_INTRA_DAY_INTERVALS:
            df.index.names = ["Timestamp"]

        df.sort_index(ascending=True, inplace=True)
        df.ohlc = ohlc.__get__(df, None)

        return df


def get_column_to_idx(columns):
    columns = [
        column.upper() if column.startswith("TR") else column for column in columns
    ]
    column_to_idx = {"Date": 1}
    column_to_idx.update({column: columns.index(column) + 2 for column in columns})
    return column_to_idx


def merge_data(adc_data, hp_data, index):
    adc = adc_data[index] if index < len(adc_data) else []
    hp = hp_data[index] if index < len(hp_data) else []
    return [*adc, *hp]


def add_one_data_item_to_data(
    data_item, data, column_to_idx, columns, instrument, is_one_inst, index
):
    data_item_values = next(iter(data_item.values()))
    for data_item_value in data_item_values:
        data_item = [instrument] if is_one_inst else [index]
        data_item_value_keys = {key.casefold(): key for key in data_item_value.keys()}

        for column in columns:
            column_casefold = column.casefold()
            if column_casefold in data_item_value_keys:
                data_item.insert(
                    column_to_idx[column],
                    data_item_value.get(data_item_value_keys[column_casefold]),
                )

            else:
                data_item.insert(column_to_idx[column], None)

        data.append(data_item)


def add_many_data_item_to_data(
    data_item, data, column_to_idx, columns, instrument, is_one_inst, index, date_name
):
    for one, two in zip_longest(
        *[sorted(item, key=lambda d: d[date_name]) for item in data_item.values()],
        fillvalue=None,
    ):
        data_item = [instrument] if is_one_inst else [index]

        if all([one, two]):
            item = {**one, **two}

        else:
            item = one or two

        key_casefold_to_key_map = {key.casefold(): key for key in item.keys()}
        for column in columns:
            column_casefold = column.casefold()
            if column_casefold in key_casefold_to_key_map.keys():
                data_item.insert(
                    column_to_idx[column],
                    item.get(key_casefold_to_key_map[column_casefold]),
                )

            else:
                data_item.insert(column_to_idx[column], None)

        data.append(data_item)


def prepare_data(
    adc_data: List[list],
    hp_data: List[list],
    instruments: "UniverseContainer",
    columns: List[str],
    date_name: str,
) -> List[list]:

    is_one_inst = len(instruments) == 1
    data = []
    column_to_idx = get_column_to_idx(columns)

    for index, instrument in enumerate(instruments):
        merged_data = merge_data(adc_data, hp_data, index)
        unique_dates = list(dict.fromkeys([item[date_name] for item in merged_data]))
        columns = column_to_idx.keys()

        for date_item in unique_dates:
            group_items = groupby(
                [item for item in merged_data if item[date_name] == date_item],
                lambda item: item["Type"],
            )

            data_item = {}
            for item_type, items in group_items:
                data_item[item_type] = list(items)

            if len(data_item) == 1:
                add_one_data_item_to_data(
                    data_item,
                    data,
                    column_to_idx,
                    columns,
                    instrument,
                    is_one_inst,
                    index,
                )

            else:
                add_many_data_item_to_data(
                    data_item,
                    data,
                    column_to_idx,
                    columns,
                    instrument,
                    is_one_inst,
                    index,
                    date_name,
                )

    return data


def chunks(generator, chunk_size):
    """Yield successive chunks from a generator"""
    chunk = []

    for item in generator:
        if len(chunk) >= chunk_size:
            yield chunk
            chunk = [item]
        else:
            chunk.append(item)

    if chunk:
        yield chunk


def group_universe(universe: List[str]) -> List[tuple]:
    valid_universe = (
        i for i in universe if not (i.startswith("0#.") or i.startswith("Peers("))
    )
    return [(name, len(list(items))) for name, items in groupby(valid_universe)]
