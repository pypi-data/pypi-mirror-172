from typing import TYPE_CHECKING

from .._content_provider import ContentUsageLoggerMixin
from .._content_type import ContentType
from ..._tools import validate_bool_value
from ...delivery._data._data_provider import (
    DataProviderLayer,
    BaseResponse,
    UniverseData,
)

if TYPE_CHECKING:
    from ...content._types import ExtendedParams, StrStrings


class Definition(
    ContentUsageLoggerMixin[BaseResponse[UniverseData]],
    DataProviderLayer[BaseResponse[UniverseData]],
):
    """
    This class describe parameters to retrieve the organization information for the requested instrument.

    Parameters
    ----------
    universe: str, list of str
        The Universe parameter allows the user to define the companies for which the content is returned.

    use_field_names_in_headers: bool, optional
        Return field name as column headers for data instead of title

    extended_params : ExtendedParams, optional
        If necessary other parameters.

    Examples
    --------
    >>> from refinitiv.data.content import ownership
    >>> definition = ownership.org_info.Definition("TRI.N")
    >>> response = definition.get_data()
    """

    def __init__(
        self,
        universe: "StrStrings",
        use_field_names_in_headers: bool = False,
        extended_params: "ExtendedParams" = None,
    ):
        validate_bool_value(use_field_names_in_headers)

        super().__init__(
            ContentType.OWNERSHIP_ORG_INFO,
            universe=universe,
            use_field_names_in_headers=use_field_names_in_headers,
            extended_params=extended_params,
        )
