from typing import TYPE_CHECKING

from .._definition import BaseSurfaceDefinition
from ..._surfaces._cap_surface_request_item import CapSurfaceRequestItem
from ...._content_type import ContentType

if TYPE_CHECKING:
    from ..._surfaces._surface_types import SurfaceParameters, SurfaceLayout
    from ...._types import ExtendedParams, OptStr


class Definition(BaseSurfaceDefinition):
    def __init__(
        self,
        surface_layout: "SurfaceLayout" = None,
        surface_parameters: "SurfaceParameters" = None,
        underlying_definition: dict = None,
        surface_tag: "OptStr" = None,
        instrument_type=None,
        extended_params: "ExtendedParams" = None,
    ):
        request_item = CapSurfaceRequestItem(
            instrument_type=instrument_type,
            surface_layout=surface_layout,
            surface_params=surface_parameters,
            underlying_definition=underlying_definition,
            surface_tag=surface_tag,
        )
        super().__init__(
            content_type=ContentType.SURFACES,
            universe=request_item,
            extended_params=extended_params,
        )
