import os
from jigsawstack import JigsawStack
import logging
import sys

# Enable detailed debug logging
logging.basicConfig(level=logging.DEBUG, 
                   format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                   stream=sys.stdout)

# Initialize the client with your API key
api_key = "sk_6b0e5f86bcf014f4354cf617404a20422392d2a0115cd2520057fea5c3fdf8ce9ff0b972791649962937cb3cb167d0437bc7fdf61b99627bc838729b8037589f024rIVykPhD2e5VthayPN"
jigsaw = JigsawStack(api_key=api_key)

# Test text to speech
try:
    print("Making text-to-speech request...")
    result = jigsaw.audio.text_to_speech({
        "text": "Hello, how are you doing?",
    })
    
    # Check response type
    print(f"Response type: {type(result)}")
    print(f"Response keys: {result.keys() if hasattr(result, 'keys') else 'No keys'}")
    
    # Save the audio file
    if result and isinstance(result, dict) and 'audio_data' in result:
        with open("output.mp3", "wb") as f:
            f.write(result["audio_data"])
        print(f"Audio saved successfully with content type: {result.get('content_type')}")
        print(f"Audio size: {len(result['audio_data'])} bytes")
    else:
        print("No audio data received in response")
        print(f"Response contents: {result}")
    
except Exception as e:
    print(f"Error: {str(e)}")
    import traceback
    traceback.print_exc()
