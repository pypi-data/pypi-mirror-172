import itertools
from typing import Optional, Dict, Any, Set

import pandas as pd
from humps import pascalize

from refinitiv.data._tools import inspect_parameters_without_self
from refinitiv.data._tools.templates import StringTemplate
from refinitiv.data.content.search import Definition, Views


class SearchTemplate:
    """Discovery search preset

    Initialized with default values for content.search.Definition.
    Any string value acts as template string. You can use placeholder variables,
    and that variables will be required to prepare search parameters through
    `._search_kwargs()` or to launch search through `.search()`.

    Placeholder variables syntax:
    - Prepend variable name with # symbol: #varname
    - If after variable name must come alphanumeric symbol or _, that can be interpreted
      like a part of variable name - use curly braces: #{varname}
    - Or you can use hash with curly braces all the time, if you want
    - Hash symbol escaped with itself. '##' will be interpreted as '#'.

    Attributes
    ----------

    name: str
        name of the template

    Examples
    --------

    >>> SearchTemplate(filter="ExchangeName xeq '#name'")._search_kwargs(name="<name>")
    {'filter': "ExchangeName xeq '<name>'"}
    >>> SearchTemplate(filter="ExchangeName xeq '#name'")._search_kwargs()
    Traceback (most recent call last):
        ...
    KeyError: 'Those keyword arguments must be defined, but they are not: name'
    >>> SearchTemplate(filter="ExchangeName xeq '#{name}'", placeholders_defaults={"name": "<name>"})._search_kwargs()
    {'filter': "ExchangeName xeq '<name>'"}
    """

    def __init__(
        self,
        name=None,
        placeholders_defaults: Optional[Dict[str, Any]] = None,
        pass_through_defaults: Optional[Dict[str, Any]] = None,
        **search_defaults,
    ):
        """
        Parameters
        ----------
        name : str, optional
            name of the template
        placeholders_defaults: dict, optional
            <placeholder_name> : <placeholder_default_value>
        search_defaults
            default values for discovery search Definition
        """
        self._available_search_kwargs = inspect_parameters_without_self(Definition)
        """ List search keyword arguments we can use in this template """
        self._placeholders_defaults = (
            {} if placeholders_defaults is None else placeholders_defaults
        )
        """ Default template variables values for a templated defaults """
        if pass_through_defaults is None:
            pass_through_defaults = {}

        bad_pass_through_params = (
            set(pass_through_defaults) - self._available_search_kwargs
        )
        if bad_pass_through_params:
            raise ValueError(
                "All the parameters described in 'parameters' section of search "
                "template configuration, must be either placeholders variables or "
                "parameters of the discovery search Definition. Those parameters are "
                "neither of them: " + ", ".join(bad_pass_through_params)
            )

        self.name = name

        unknown_defaults = set(search_defaults) - set(self._available_search_kwargs)
        if unknown_defaults:
            raise ValueError(
                "This arguments are defined in template, but not in search Definition: "
                + ", ".join(unknown_defaults)
            )
        # Names of all placeholders inside string templates
        """Set of names for all placeholders in string templates"""
        self._placeholders_names: Set[str] = set()
        # Arguments to be passed to Definition as templates
        self._templated_defaults: Dict[str, StringTemplate] = {}
        # Arguments to be directly passed to Definition without any preprocessing
        self._pass_through_defaults: Dict[str, Any] = {}

        for name, value in search_defaults.items():

            if not isinstance(value, str):
                self._pass_through_defaults[name] = value
                continue

            template = StringTemplate(value)
            template.validate(prefix=f'Parameter "{name}": ')
            if template.names():
                self._templated_defaults[name] = template
                self._placeholders_names |= template.names()
            else:
                self._pass_through_defaults[name] = value

        self._pass_through_defaults.update(pass_through_defaults)

        bad_tpl_var_names = self._placeholders_names & self._available_search_kwargs
        if bad_tpl_var_names:
            raise ValueError(
                "You can't use template arguments with the same name"
                " as search arguments. You are used: " + ", ".join(bad_tpl_var_names)
            )

    def _defaults(self):
        return itertools.chain(self._templated_defaults, self._pass_through_defaults)

    def __repr__(self):
        return f"<SearchTemplate '{self.name}'>"

    def _search_kwargs(self, **kwargs) -> dict:
        """Get dictionary of arguments for content.search.Definition"""

        undefined_placeholders = (
            self._placeholders_names - set(kwargs) - set(self._placeholders_defaults)
        )

        if undefined_placeholders:
            raise KeyError(
                "Those keyword arguments must be defined, but they are not: "
                + ", ".join(undefined_placeholders)
            )

        unexpected_arguments = (
            set(kwargs)
            - self._placeholders_names
            # templated defaults can't be redefined
            - (self._available_search_kwargs - self._templated_defaults.keys())
        )

        if unexpected_arguments:
            raise KeyError(f"Unexpected arguments: {', '.join(unexpected_arguments)}")

        kwargs = kwargs.copy()
        # Applying template variables defaults
        for name, value in self._placeholders_defaults.items():
            if name not in kwargs:
                kwargs[name] = value

        result = self._pass_through_defaults.copy()

        # Apply variables to templated defaults
        for name, template in self._templated_defaults.items():
            result[name] = template.substitute(**kwargs)

        # Apply other variables from kwargs
        for name, value in kwargs.items():
            if name not in self._placeholders_names:
                result[name] = value

        return result

    def search(self, **kwargs) -> pd.DataFrame:
        """Please, use help() on a template object itself to get method documentation"""
        # ^ we need this docstring because we can't easily generate docstring for
        # the method, but can change __doc__ for class instance
        return Definition(**self._search_kwargs(**kwargs)).get_data().data.df

    def export(self) -> dict:
        """Get dictionary that can be used in config to duplicate this template

        Or use it as a base for another search template.
        Exported without documentation.
        """
        request_body = pascalize(self._pass_through_defaults)
        request_body.update({pascalize(k): v.template for k, v in self._templated_defaults.items()})

        if "View" in request_body and isinstance(request_body["View"], Views):
            request_body["View"] = request_body["View"].value

        result = {"request_body": request_body}

        if self._placeholders_defaults:
            result["parameters"] = {
                name: {"default": value}
                for name, value in self._placeholders_defaults.items()
            }

        return result
