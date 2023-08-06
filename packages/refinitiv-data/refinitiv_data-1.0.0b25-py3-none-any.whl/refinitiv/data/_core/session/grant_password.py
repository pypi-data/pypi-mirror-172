# coding: utf-8

from .grant import Grant
from .tools import Sensitive


class GrantPassword(Grant):
    def __init__(self, *args, **kwargs):
        """

        Parameters
        ----------
        *args: iterable
            args[0] is username, args[1] is password, args[2] is token scope (default: "trapi")
        **kwargs
            username: str, password: str

        Examples
        --------
        >>> import refinitiv.data as rdp
        >>> rdp.session.platform.GrantPassword(username="username", password="password", token_scope="token_scope")
        or
        >>> import refinitiv.data as rdp
        >>> rdp.session.platform.GrantPassword("username", "password", "token_scope")

        """
        super(GrantPassword, self).__init__(*args, **kwargs)

        if len(args) == 2:
            self._password = Sensitive(args[1])
        elif "password" in kwargs:
            self._password = Sensitive(kwargs["password"])

        self._token_scope = ""

        if len(args) == 3:
            self._token_scope = args[2]
        else:
            self._token_scope = kwargs.get("token_scope", "trapi")

        default_scope = "trapi"
        self._token_scope = self._token_scope or default_scope

    def get_password(self):
        return self._password

    def password(self, value):
        self._password = Sensitive(value)
        return self

    def get_token_scope(self):
        return self._token_scope

    def with_scope(self, token_scope):
        if token_scope:
            self._token_scope = token_scope
        return self

    def is_valid(self):
        return self._password and self._username
