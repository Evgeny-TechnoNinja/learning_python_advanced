from typing import Union


class UrlFormatError(Exception):
    """
    Implements error output for invalid url
    """

    def __init__(self, element: str):
        self.element = element

    def __str__(self):
        return f"Error, invalid data here {self.element}"


class Url:
    """
    Implements a URL string that is a pointer to a resource
    """
    __reserved_schemes: list = ["http", "https"]
    _url: str = ""

    def __init__(self, scheme: str, authority: str, path: Union[str, list] = "", query: Union[str, dict] = "",
                 fragment: str = ""):
        self._scheme = scheme
        self._authority = authority
        self._path = path
        self._query = query
        self._fragment = fragment
        self._create_url()

    def __eq__(self, other):
        return self._url == other

    def __str__(self):
        return self._url

    def _schema_validation(self):
        if self._scheme in self.__reserved_schemes:
            self._url += f"{self._scheme}://"
        else:
            raise UrlFormatError(self._scheme)

    def _analysis_authority(self):
        separator, ban = ":", "!@#$%^&*()+_"
        if any((mark in ban) for mark in self._authority):
            raise UrlFormatError(self._authority)

        if separator in self._authority and self._authority.count(separator) == 1:
            aut_data: list = self._authority.split(separator)
            if aut_data[-1].isdigit():
                self._url += f"{aut_data[0]}{separator}{aut_data[-1]}"
        else:
            self._url += f"{self._authority}"

        if self._path:
            self._url += "/"

    def _build_path(self):
        separator = "/"
        if isinstance(self._path, list):
            self._url += "/".join(self._path)
        elif isinstance(self._path, str):
            if separator in self._path and len(self._path) > 1:
                self._url += "/".join([elem for elem in self._path.split(separator) if elem != ""])
            else:
                self._url += self._path

    def _build_query(self):
        separator, query_start = "&", "?"
        self._url += query_start
        if isinstance(self._query, str):
            self._url += f"{self._query}"
        elif isinstance(self._query, dict):
            count: int = len(self._query.items())
            for current_key, current_value in self._query.items():
                self._url += f"{current_key}={current_value}"
                if count > 1:
                    self._url += separator
                    count -= 1
        else:
            raise UrlFormatError(str(self._query))

    def _build_fragment(self):
        fragment_start = "#"
        self._url += f"{fragment_start}{self._fragment}"

    def _create_url(self):
        """
        builds url string, a pointer to a resource
        _url - will receive a string
        do not change the order in which functions are run
        """
        self._schema_validation()
        self._analysis_authority()
        if self._path:
            self._build_path()
        if self._query:
            self._build_query()
        if self._fragment:
            self._build_fragment()


class HttpsUrl(Url):
    __scheme = "https"

    def __init__(self, authority: str, path: Union[str, list] = "", query: Union[str, dict] = "", fragment: str = ""):
        super().__init__(scheme=self.__scheme, authority=authority, path=path, query=query, fragment=fragment)


class HttpUrl(Url):
    __scheme = "http"

    def __init__(self, authority: str, path: Union[str, list] = "", query: Union[str, dict] = "", fragment: str = ""):
        super().__init__(scheme=self.__scheme, authority=authority, path=path, query=query, fragment=fragment)


class GoogleUrl(Url):
    __scheme = "https"
    __authority = "google.com"

    def __init__(self, path: Union[str, list] = "", query: Union[str, dict] = "", fragment: str = ""):
        super().__init__(scheme=self.__scheme, authority=self.__authority, path=path, query=query, fragment=fragment)


class WikiUrl(Url):
    __scheme = "https"
    __authority = "wikipedia.org"

    def __init__(self, path: Union[str, list] = "", query: Union[str, dict] = "", fragment: str = ""):
        super().__init__(scheme=self.__scheme, authority=self.__authority, path=path, query=query, fragment=fragment)


# === GoogleUrl test ==
assert GoogleUrl() == HttpsUrl(authority="google.com")
assert GoogleUrl() == Url(scheme="https", authority="google.com")
assert GoogleUrl() == "https://google.com"
assert GoogleUrl(query={'q': 'python', 'result': 'json'}) == 'https://google.com?q=python&result=json'
# ===
# === WikiUrl test ==
assert WikiUrl() == str(Url(scheme='https', authority='wikipedia.org'))
assert WikiUrl(path=['wiki', 'python']) == 'https://wikipedia.org/wiki/python'
# ===
