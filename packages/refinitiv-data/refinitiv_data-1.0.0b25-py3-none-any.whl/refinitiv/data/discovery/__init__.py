__all__ = ("search", "Views", "search_templates")

from ._search import search
from ..content.search import Views
from ._search_templates import templates as search_templates
