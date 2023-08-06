import abc
from typing import TYPE_CHECKING, Optional, List, Union, Dict

from pandas import DataFrame

from ...content._df_builder import dfbuilder_rdp, dfbuilder_udf

if TYPE_CHECKING:
    from ...content._df_builder import DFBuilder
    from .._containers import (
        FieldsContainer,
        UniverseContainer,
        ADCDataContainer,
        HPDataContainer,
        CustInstDataContainer,
    )


class Context(abc.ABC):
    def __init__(
        self, universe: "UniverseContainer", fields: "FieldsContainer"
    ) -> None:
        self.fields = fields
        self.universe = universe
        self._data: Optional[list] = []
        self._headers: Optional[List[List[str]]] = None
        self._adc_data: Optional["ADCDataContainer"] = None
        self._hp_data: Optional["HPDataContainer"] = None
        self._cust_inst_data: Optional["CustInstDataContainer"] = None

    def set_data(
        self,
        adc_data: "ADCDataContainer",
        hp_data: "HPDataContainer",
        cust_inst_data: "CustInstDataContainer",
    ):
        self._adc_data = adc_data
        self._hp_data = hp_data
        self._cust_inst_data = cust_inst_data

    @property
    @abc.abstractmethod
    def dfbuilder(self) -> "DFBuilder":
        # for override
        pass

    @property
    @abc.abstractmethod
    def date_name(self) -> str:
        #  for override
        pass

    @property
    def data(self) -> list:
        return self._data

    @property
    def headers(self) -> List[List[str]]:
        return self._headers

    @property
    @abc.abstractmethod
    def raw(self) -> Optional[Dict]:
        # for override
        pass

    @property
    @abc.abstractmethod
    def df(self) -> Optional[DataFrame]:
        # for override
        pass

    @property
    @abc.abstractmethod
    def can_get_data(self) -> bool:
        # for override
        pass

    @property
    @abc.abstractmethod
    def can_build_df(self) -> bool:
        # for override
        pass

    @abc.abstractmethod
    def build_df(self, use_field_names_in_headers: bool, *args) -> DataFrame:
        # for override
        pass

    @abc.abstractmethod
    def prepare_to_build(
        self, interval, use_field_names_in_headers, df, headers, *args
    ):
        # for override
        pass

    @abc.abstractmethod
    def prepare_data(self, raw, fields, *args) -> list:
        # for override
        pass

    @abc.abstractmethod
    def prepare_headers(self, raw: Union[list, dict], *args) -> List[List[str]]:
        # for override
        pass


class RDPMixin:
    @property
    def dfbuilder(self):
        return dfbuilder_rdp

    @property
    def date_name(self) -> str:
        return "date"


class UDFMixin:
    @property
    def dfbuilder(self):
        return dfbuilder_udf

    @property
    def date_name(self) -> str:
        return "Date"
