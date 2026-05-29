# src/config.py
import os
from dotenv import load_dotenv

load_dotenv()

ANTHROPIC_API_KEY   = os.environ["ANTHROPIC_API_KEY"]
ELEVENLABS_API_KEY  = os.environ["ELEVENLABS_API_KEY"]
ELEVENLABS_VOICE_ID = os.environ["ELEVENLABS_VOICE_ID"]
PEXELS_API_KEY      = os.environ["PEXELS_API_KEY"]
YOUTUBE_CREDS_JSON  = os.environ["YOUTUBE_CREDENTIALS_JSON"]

OUTPUT_DIR   = "output"
AUDIO_DIR    = f"{OUTPUT_DIR}/audio"
CLIPS_DIR    = f"{OUTPUT_DIR}/clips"
VIDEOS_DIR   = f"{OUTPUT_DIR}/videos"
