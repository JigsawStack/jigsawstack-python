from typing import Dict, Union


class ClientConfig:
    base_url: str
    api_key: str
    headers: Union[Dict[str, str], None]

    def __init__(
        self,
        api_key: str,
        base_url: str,
        headers: Union[Dict[str, str], None] = None,
    ):
        self.api_key = api_key
        self.base_url = base_url
        self.headers = headers
