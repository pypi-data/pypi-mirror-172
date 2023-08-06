from enum import Enum, auto
from typing import TYPE_CHECKING, Union

from ._adc_context import ADCContext
from ._adc_rdp_context import ADCRDPContext
from ._adc_udf_context import ADCUDFContext
from ._cust_inst_context import CustInstContext
from ._cust_inst_rdp_context import CustInstRDPContext
from ._cust_inst_udf_context import CustInstUDFContext
from ._hp_context import HPContext
from ._hp_rdp_context import HPRDPContext
from ._hp_udf_context import HPUDFContext
from ...content.fundamental_and_reference._data_grid_type import DataGridType

if TYPE_CHECKING:
    from .._containers import (
        FieldsContainer,
        UniverseContainer,
    )


class ContextType(Enum):
    ADC = auto()
    HP = auto()
    CustInst = auto()


data_grid_type_by_context_class_by_context_type = {
    ContextType.ADC: {
        DataGridType.UDF: ADCUDFContext,
        DataGridType.RDP: ADCRDPContext,
    },
    ContextType.HP: {
        DataGridType.UDF: HPUDFContext,
        DataGridType.RDP: HPRDPContext,
    },
    ContextType.CustInst: {
        DataGridType.UDF: CustInstUDFContext,
        DataGridType.RDP: CustInstRDPContext,
    },
}


def get_context(
    context_type: ContextType,
    data_grid_type: "DataGridType",
    universe: "UniverseContainer",
    fields: "FieldsContainer",
) -> Union[CustInstContext, ADCContext, HPContext]:
    data_grid_type_by_context_class = (
        data_grid_type_by_context_class_by_context_type.get(context_type)
    )

    if not data_grid_type_by_context_class:
        raise TypeError(f"Unexpected context_type. Type: {context_type}")

    context_class = data_grid_type_by_context_class.get(data_grid_type)

    if not context_class:
        raise TypeError(f"Unexpected type. Type: {data_grid_type}")

    return context_class(universe, fields)


def get_cust_inst_context(
    data_grid_type: "DataGridType",
    universe: "UniverseContainer",
    fields: "FieldsContainer",
) -> CustInstContext:
    return get_context(ContextType.CustInst, data_grid_type, universe, fields)


def get_adc_context(
    data_grid_type: "DataGridType",
    universe: "UniverseContainer",
    fields: "FieldsContainer",
) -> ADCContext:
    return get_context(ContextType.ADC, data_grid_type, universe, fields)


def get_hp_context(
    data_grid_type: "DataGridType",
    universe: "UniverseContainer",
    fields: "FieldsContainer",
) -> HPContext:
    return get_context(ContextType.HP, data_grid_type, universe, fields)
