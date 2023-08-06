from user_agent import generate_user_agent
from json.decoder import JSONDecodeError
from requests import Session, Response
from bs4 import BeautifulSoup

import json

from .logger import Logger


class FractifClient(Session):
    ua: str = generate_user_agent()
    soup: BeautifulSoup = None
    json: dict = None
    res_type: str = None  # 'json' or 'html'

    def __init__(self, BASEURL: str = None, debug: bool = True):
        Session.__init__(self)

        self.BASEURL = BASEURL
        self.verify = False
        self.logger = Logger('urllib3') if debug else None
        self.headers = {
            'User-Agent': self.ua,
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
        }

    def __str__(self) -> str:
        return f'<FractifClient {self.headers["User-Agent"]}>'

    def clean(self) -> None:
        self.soup = None
        self.json = None
        self.res_type = None

    def build_soup(self, html: str) -> BeautifulSoup:
        return BeautifulSoup(html, 'lxml')

    def build_json(self, content: str) -> dict:
        try:
            return json.loads(content)
        except JSONDecodeError:
            raise Exception('Invalid JSON', content)

    def parse_response(self, response: Response) -> None:
        content_type = response.headers.get('content-type')
        if 'application/json' in content_type:
            self.res_type = 'json'
            self.json = self.build_json(response.text)
        elif 'text/html' in content_type:
            self.res_type = 'html'
            self.soup = self.build_soup(response.text)
        else:
            raise Exception('Unknown content type')

    def go(
        self,
        url,
        data=None,
        method='GET',
        headers=None,
        params=None,
        cookies=None,
        proxies=None,
        allow_redirects=True,
        *args,
        **kwargs
    ) -> Response:
        """
        Request to go on this url.

        Arguments are optional parameters for url.
        >>> self.go('https://example.com')
        """
        if not url.startswith('https://'):
            url = self.BASEURL + url
        res = self.request(
            method,
            url,
            data=data,
            headers=headers,
            params=params,
            cookies=cookies,
            allow_redirects=allow_redirects,
            proxies=proxies,
            *args,
            **kwargs
        )
        res.raise_for_status()
        self.parse_response(res)
        return res
