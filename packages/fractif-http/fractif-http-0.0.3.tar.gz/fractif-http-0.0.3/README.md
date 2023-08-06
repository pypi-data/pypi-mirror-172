
# Fractif HTTP

Simple, yet elegant, HTTP library. As like as Requests.
Actually, it is based on requests package...

```python
from fractifhttp import FractifClient


class Example(FractifClient):
    BASEURL = 'https://example.com'

    search = '/search'
    api = '/api/v1'

    def __init__(self, debug=True, *args, **kwargs):
        super().__init__(self.BASEURL, debug, *args, **kwargs)
        self.logger = Logger('example').logger

    def get_search(self, query):
        self.go(self.search, params={'q': query})
        print(self.soup.title.text)
        # Example Domain

    def get_api(self):
        self.go(self.api)
        print(self.json)
        # {'success': True}
```


## Installation

Install fractif-http with pip

```bash
pip install fractif-http
```

## TODO

- Add URL object (easier url navigation)
