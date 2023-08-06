from typing import Optional, Iterable, Union

from ._enums import ForwardCurvesOutputs
from ._forward_curve_definition import ForwardCurveDefinition
from ._models import Step, Turn
from ._swap_zc_curve_definition import SwapZcCurveDefinition
from ._swap_zc_curve_parameters import SwapZcCurveParameters
from ..curves import forward_curves
from ..._types import Strings

CurveDefinition = Optional[SwapZcCurveDefinition]
CurveParameters = Optional[SwapZcCurveParameters]
ForwardCurveDefinitions = Union[
    ForwardCurveDefinition, Iterable[ForwardCurveDefinition]
]
OptForwardCurveDefinitions = Optional[ForwardCurveDefinitions]

Outputs = Union[Strings, Iterable[ForwardCurvesOutputs]]
Universe = Union[forward_curves.Definition, Iterable[forward_curves.Definition]]

Steps = Union[Iterable[Step]]
Turns = Union[Iterable[Turn]]
