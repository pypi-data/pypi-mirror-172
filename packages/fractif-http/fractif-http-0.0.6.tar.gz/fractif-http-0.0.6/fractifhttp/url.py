from requests import Response

import requests
import re

from .regex_helper import normalize


class UrlNotResolvable(Exception):
    """
    Raised when trying to locate on an URL instance
    which url pattern is not resolvable as a real url.
    """


class URL(object):
    _creation_counter = 0

    def __init__(self, *args):
        self.urls = []
        self.klass = None
        self.browser = None
        for arg in args:
            if isinstance(arg, str):
                self.urls.append(arg)
            if isinstance(arg, type):
                self.klass = arg

        self._creation_counter = URL._creation_counter
        URL._creation_counter += 1

    def go(
        self,
        *,
        params=None,
        data=None,
        json=None,
        method='GET',
        headers=None,
        **kwargs
    ) -> Response:
        """
        Request to go on this url.

        Arguments are optional parameters for url.
        >>> self.go('https://example.com')
        """
        return self.browser.go(
            url=self.build(**kwargs),
            params=params,
            data=data,
            json=json,
            method=method,
            headers=headers or {},
        )

    def build(self, **kwargs):
        browser = kwargs.pop('browser', self.browser)
        params = kwargs.pop('params', None)
        patterns = []
        for url in self.urls:
            patterns += normalize(url)

        for pattern, _ in patterns:
            url = pattern
            args = kwargs.copy()
            for key in list(args.keys()):
                search = '%%(%s)s' % key
                if search in pattern:
                    url = url.replace(search, str(args.pop(key)))
            if re.search(r'%\([A-z_]+\)s', url):
                continue
            if len(args):
                continue

            url = browser.absurl(url, base=True)
            if params:
                p = requests.models.PreparedRequest()
                p.prepare_url(url, params)
                url = p.url
            return url

        raise UrlNotResolvable(
            'Unable to resolve URL with %r. Available are %s'
            % (kwargs, ', '.join([pattern for pattern, _ in patterns]))
        )
