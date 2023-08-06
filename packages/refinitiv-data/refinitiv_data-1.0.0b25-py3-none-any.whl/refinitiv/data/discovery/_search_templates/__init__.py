"""Module to create and use templated search presets for the discovery search

Use templated search from the "Equity" template that was defined in the config:
>>> import refinitiv.data as rd
>>> rd.content.discovery.search_templates["Equity"].search()
"""

from typing import Dict, List

from humps import depascalize

from refinitiv.data import get_config
from refinitiv.data._errors import ConfigurationError
from refinitiv.data.content.search import Views
from refinitiv.data.discovery._search_templates.embedded import (
    RICCategoryTemplate, UnderlyingRICToOptionTemplate, UnderlyingRICToFutureTemplate,
    RICToIssuerTemplate, OrganisationPermIDToUPTemplate, MinesTemplate,
    VesselsBoundForTemplate
)
from refinitiv.data.discovery._search_templates.base import SearchTemplate

__all__ = ["templates", "Templates", "SearchTemplate"]

CONFIG_PREFIX = "search.templates"


def depascalize_view(value: str) -> str:
    """Convert search View value to upper snakecase

    We need to have separate function for that because some enum View values
    does not follow the rules of pascal case
    """
    if "STIRs" in value:
        value = value.replace("STIRs", "Stirs")

    return depascalize(value).upper()


def generate_docstring(description: str, methods: Dict[str, dict]):
    doc = [
        description,
        "",
        "    Methods",
        "    -------",
    ]

    for method_name, method_desc in methods.items():
        doc.append(f"    {method_name}")

        for param, desc in method_desc["args"].items():
            doc.append(f"        {param}")
            if "description" in desc:
                doc.append(f"            {desc['description']}")
            if "default" in desc:
                doc.append(f"            default: {repr(desc['default'])}")
            doc.append("")

    return "\n".join(doc)


class Templates:
    """Easy access to search templates from the library config

    Check if search template with the name "Equity" is defined in the config:
    >>> templates = Templates()
    >>> "Equity" in templates
    True
    Get "Equity" search template:
    >>> templates["Equity"]
    Get list of available search template names:
    >>> templates.keys()
    ["Equity"]
    """

    RICCategory = RICCategoryTemplate()
    UnderlyingRICToOption = UnderlyingRICToOptionTemplate()
    UnderlyingRICToFuture = UnderlyingRICToFutureTemplate()
    RICToIssuer = RICToIssuerTemplate()
    OrganisationPermIDToUP = OrganisationPermIDToUPTemplate()
    Mines = MinesTemplate()
    VesselsBoundFor = VesselsBoundForTemplate()

    def __iter__(self):
        config = get_config()
        return config.get(CONFIG_PREFIX, {}).keys().__iter__()

    @staticmethod
    def _from_data(name, data):
        # <param_name>: {"default": <default>, "description": <doc>}
        tpl_strs_defaults = {
            name: attrs["default"]
            for name, attrs in data.get("parameters", {}).items()
            if "default" in attrs
        }
        params = depascalize(data.get("request_body", {}))

        if "view" in params:
            # Convert string value to enum for the view argument
            view = params["view"]
            try:
                params["view"] = getattr(Views, depascalize_view(view))
            except AttributeError:
                raise ConfigurationError(
                    -1,
                    f"Wrong search template value: View={view}. "
                    "It must be one of the following: "
                    f"{', '.join(Views.possible_values())}",
                )
        tpl = SearchTemplate(name, placeholders_defaults=tpl_strs_defaults, **params)

        method_args = {}
        # Some placeholders may be only in string, but not in "parameters"
        for param in sorted(tpl._placeholders_names):
            method_args[param] = data.get("parameters", {}).get(param, {})

        # That's why we can get them all in one cycle with pass-through parameters
        # that is located in "parameters" config session, but not in template string
        for param, desc in data.get("parameters", {}).items():
            if param not in tpl._placeholders_names:
                method_args[param] = desc

        tpl.__doc__ = generate_docstring(
            description=data.get("description", ""),
            methods={"search": {"description": "", "args": method_args}},
        )

        return tpl

    def __getitem__(self, name: str) -> SearchTemplate:
        config = get_config()
        key = f"{CONFIG_PREFIX}.{name}"
        if key not in config:
            raise KeyError(f"Template '{name}' is not found in the config")
        data = config[key].as_attrdict() if config[key] is not None else {}

        return self._from_data(name, data)

    def keys(self) -> List[str]:
        """Get list of available search template names"""
        return list(self)


templates = Templates()
