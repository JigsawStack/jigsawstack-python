class ClientConfig:

    base_url:str
    api_key:str
    
    def __init__(self, api_key: str, api_url: str):
        self.api_key = api_key
        self.api_url = api_url