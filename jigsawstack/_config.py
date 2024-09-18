from typing import Union


class ClientConfig:
    base_url: str
    api_key: str
    disable_request_logging: Union[bool, None] = None

    def __init__(
        self,
        api_key: str,
        api_url: str,
        disable_request_logging: Union[bool, None] = None,
    ):
        self.api_key = api_key
        self.api_url = api_url
        self.disable_request_logging = disable_request_logging
