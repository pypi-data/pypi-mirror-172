from datetime import date, datetime, timedelta
from typing import Optional, Callable, List, Union

OptStr = Optional[str]
Strings = List[str]
Dicts = List[dict]
OptStrings = Optional[Strings]
OptDicts = Optional[Dicts]

OptInt = Optional[int]
OptFloat = Optional[float]
OptList = Optional[list]
OptTuple = Optional[tuple]
OptDict = Optional[dict]
OptSet = Optional[set]
OptBool = Optional[bool]
OptCall = Optional[Callable]

ExtendedParams = OptDict
StrStrings = Union[str, Strings]
OptStrStrs = Optional[StrStrings]
DateTime = Union[str, date, datetime, timedelta]
OptDateTime = Optional[DateTime]
