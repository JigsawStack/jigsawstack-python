# JigsawStack Python SDK

## Installation

To install JigsawStack Python SDK, simply execute the following command in a terminal:

```
pip install jigsawstack
```

## Setup

First, you need to get an API key, which is available in the [JigsawStack Dashboard](https://jigsawstack.com).

```py
from jigsawstack from JigsawStack

import os

 ai = JigsawStack(api_key="your-api-key")
```

## Example

```py
import os
from jigsawstack from JigsawStack


ai = JigsawStack(api_key="your-api-key")

params = {
    "url": "https://rogilvkqloanxtvjfrkm.supabase.co/storage/v1/object/public/demo/Collabo%201080x842.jpg?t=2024-03-22T09%3A22%3A48.442Z"
}

result = ai.vision.vocr(params)

print(result)
```
