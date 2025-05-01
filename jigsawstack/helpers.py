
from typing import Dict, Optional, Union
from urllib.parse import urlencode

def build_path(base_path: str, params: Optional[Dict[str, Union[str, int, bool]]] = None) -> str:
    """
    Build an API endpoint path with query parameters.

    Args:
        base_path (str): The base path endpoint (e.g. '/store/file')
        params (Optional[Dict[str, Union[str, int, bool]]]): A dictionary of query parameters

    Returns:
        str: The constructed path with query parameters
    """
    if params is None:
        return base_path
    
    #remove None values from the parameters
    filtered_params = { k: str(v).lower() if isinstance(v, bool) else v for k, v in params.items() if v is not None}

    #encode the parameters
    return f"{base_path}?{urlencode(filtered_params)}" if filtered_params else base_path


