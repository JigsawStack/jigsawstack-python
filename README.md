# JigsawStack Python SDK

The JigsawStack Python SDK allows you to interact with powerful AI services to build AI-powered applications.

- 🧩 Powerful AI services all in one SDK
- ⌨️ Fully typed parameters and responses
- 📡 Built in Webhook support for long-running tasks
- 📦 Built in file system for easy file uploads

## Learn more

To learn more about all available JigsawStack AI services, view the [Documentation](https://docs.jigsawstack.com) or [Website](https://jigsawstack.com).

## All APIs

| Category          | APIs                                              |
| ----------------- | ------------------------------------------------- |
| **👉 General**    | Translation, Summarization, Sentiment Analysis    |
| **🌐 Web**        | AI Web Scraping, AI Web Search                    |
| **🎵 Audio**      | Text to Speech, Speech to Text (Whisper large v3) |
| **👀 Vision**     | vOCR, Object Detection                            |
| **🧠 LLMs**       | Prompt Engine                                     |
| **🖼️ Generative** | AI Image (SD, SDXL-Fast & more), HTML to Any      |
| **🌍 Geo**        | Location search, Timezone, IP Geolocation & more  |
| **✅ Validation** | Email, NSFW images, profanity & more              |
| **📁 Store**      | Simple File Storage, KV Encryption store          |

Learn more of about each category in the [API reference](https://docs.jigsawstack.com/api-reference)

## Installation

To install JigsawStack Python SDK, simply execute the following command in a terminal:

```
pip install jigsawstack
```

## Setup

First, get your API key from the [JigsawStack Dashboard](https://jigsawstack.com/dashboard)

Then, initialize the SDK:

```py
from jigsawstack import JigsawStack

jigsaw = JigsawStack(api_key="your-api-key")
```

## Usage

AI Scraping Example:

```py
params = {
 "url": "https://www.amazon.com/Cadbury-Mini-Caramel-Eggs-Bulk/dp/B0CWM99G5W",
 "element_prompts": ["prices"]
}
result = jigsaw.web.ai_scrape(params)
```

Text To Speech Example:

```py
params = {"text": "Hello, how are you doing?"}
result = jigsaw.audio.text_to_speech(params)
```

Speech To Text Example:

```py
params = { "url": "https://rogilvkqloanxtvjfrkm.supabase.co/storage/v1/object/public/demo/Video%201737458382653833217.mp4?t=2024-03-22T09%3A50%3A49.894Z"}
result = jigsaw.audio.speech_to_text(params)
```

VOCR:

```py
params = {
    "url": "https://rogilvkqloanxtvjfrkm.supabase.co/storage/v1/object/public/demo/Collabo%201080x842.jpg?t=2024-03-22T09%3A22%3A48.442Z"
}
result = jigsaw.vision.vocr(params)
```

## Community

Join JigsawStack community on [Discord](https://discord.gg/dj8fMBpnqd) to connect with other developers, share ideas, and get help with the SDK.

## Related Projects

- [Docs](https://docs.jigsawstack.com)
- [Javascript SDK](https://github.com/JigsawStack/jigsawstack-js)

## Contributing

JigsawStack AI SDK is open-source and welcomes contributions. Please open an issue or submit a pull request with your changes. Make sure to be as descriptive as possible with your submissions, include examples if relevant.
