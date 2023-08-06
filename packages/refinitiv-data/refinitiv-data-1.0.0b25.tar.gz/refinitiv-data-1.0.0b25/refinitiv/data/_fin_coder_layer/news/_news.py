from typing import Optional, Union

import pandas as pd

from ...content._types import OptDateTime
from ...content.news import story as _story
from ...content.news import headlines as _headlines
from ...content.news._sort_order import SortOrder


from enum import Enum, unique


@unique
class Format(Enum):
    TEXT = "Text"
    HTML = "Html"


def get_story(
    story_id: str,
    closure: Optional[str] = None,
    format: Optional[Union[Format, str]] = Format.HTML,
) -> str:
    """
    This function describes parameters to retrieve data for news story.

    Parameters
    ----------
    story_id : str
        News Story ID.
    closure : str, optional
        Specifies the parameter that will be merged with the request
    format : Format, optional
        Specifies the type of response. If parameter Format.TEXT
        return text string, otherwise returns HTML response

    Returns
    -------
    str
        Story html or text response

    Examples
    --------
    >>> import refinitiv.data as rd
    >>> response = rd.news.get_story("urn:newsml:reuters.com:20220713:nL1N2YU10J")
    """

    response = _story.Definition(story_id, closure).get_data()

    if format == Format.HTML or format == "Html":
        response = response.data.raw.get("story", {}).get("storyHtml") or response.html
    else:
        response = response.data.story.content

    return response


def get_headlines(
    query: str,
    count: int = 10,
    start: "OptDateTime" = None,
    end: "OptDateTime" = None,
    order_by: SortOrder = SortOrder.new_to_old,
) -> pd.DataFrame:
    """
    This function describes parameters to retrieve data for news headlines.

    Parameters
    ----------
    query: str
        The user search query.
    count: int, optional
        Count to limit number of headlines. Min value is 0. Default: 10
    start: str or timedelta, optional
        Beginning of date range.
        String format is: '%Y-%m-%dT%H:%M:%S'. e.g. '2016-01-20T15:04:05'.
    end: str or timedelta, optional
        End of date range.
        String format is: '%Y-%m-%dT%H:%M:%S'. e.g. '2016-01-20T15:04:05'.
    order_by: SortOrder
        Value from SortOrder enum. Default: SortOrder.new_to_old

    Returns
    -------
    pd.DataFrame
        Headlines dataframe

    Examples
    --------
    >>> from datetime import timedelta
    >>> import refinitiv.data as rd
    >>> definition = rd.news.get_headlines(
    ...     "Refinitiv",
    ...     start="20.03.2021",
    ...     end=timedelta(days=-4),
    ...     count=3
    ... )
    """

    response = _headlines.Definition(
        query=query, count=count, date_from=start, date_to=end, sort_order=order_by
    ).get_data()

    response = response.data.df

    return response
