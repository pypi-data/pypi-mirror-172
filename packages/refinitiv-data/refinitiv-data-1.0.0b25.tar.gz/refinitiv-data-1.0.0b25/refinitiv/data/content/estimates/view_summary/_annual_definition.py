from typing import Union, TYPE_CHECKING

from ..._content_provider import ContentUsageLoggerMixin
from .._enums import Package
from ..._content_type import ContentType
from ...._tools import validate_types, validate_bool_value
from ....delivery._data._data_provider import (
    DataProviderLayer,
    BaseResponse,
    UniverseData,
)

if TYPE_CHECKING:
    from ....content._types import StrStrings, ExtendedParams


class Definition(
    ContentUsageLoggerMixin[BaseResponse[UniverseData]],
    DataProviderLayer[BaseResponse[UniverseData]],
):
    """
    This class describe parameters to retrieves the annual estimates summary data for periodic estimates measures.

    Parameters
    ----------
    universe: str, list of str
        The Universe parameter allows the user to define the companies for which the content is returned.

    package: str, Package
        Packages of the content that are subsets in terms of breadth (number of fields) and depth (amount of history) of
        the overall content set. Types of packages: basic, standard, professional

    use_field_names_in_headers: bool, optional
        Return field name as column headers for data instead of title

    extended_params: ExtendedParams, optional
        If necessary other parameters.

    Examples
    --------
    >>> from refinitiv.data.content import estimates
    >>> definition = estimates.view_summary.annual.Definition(universe="IBM.N", package=estimates.Package.BASIC)
    >>> response = definition.get_data()
    """

    def __init__(
        self,
        universe: "StrStrings",
        package: Union[str, Package],
        use_field_names_in_headers: bool = False,
        extended_params: "ExtendedParams" = None,
    ):
        validate_types(package, [str, Package], "package")
        validate_bool_value(use_field_names_in_headers)

        super().__init__(
            ContentType.ESTIMATES_VIEW_SUMMARY_ANNUAL,
            universe=universe,
            package=package,
            use_field_names_in_headers=use_field_names_in_headers,
            extended_params=extended_params,
        )
