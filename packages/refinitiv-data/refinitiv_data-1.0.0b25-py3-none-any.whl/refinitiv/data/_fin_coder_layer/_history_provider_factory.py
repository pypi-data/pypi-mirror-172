from .context_collection import RDPMixin, UDFMixin
from ._history_provider import HistoryProvider
from ..content.fundamental_and_reference._data_grid_type import (
    DataGridType,
)


class HistoryRDPProvider(RDPMixin, HistoryProvider):
    pass


class HistoryUDFProvider(UDFMixin, HistoryProvider):
    pass


provider_by_data_grid_type = {
    DataGridType.UDF: HistoryUDFProvider(),
    DataGridType.RDP: HistoryRDPProvider(),
}


def get_history_provider(
    data_grid_type: "DataGridType",
) -> "HistoryProvider":
    provider = provider_by_data_grid_type.get(data_grid_type)

    if not provider:
        raise TypeError(f"Unexpected platform type. Type: {data_grid_type}")

    return provider
