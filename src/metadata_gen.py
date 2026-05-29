import os
import json
from dotenv import load_dotenv

load_dotenv()

ANTHROPIC_API_KEY   = os.environ["ANTHROPIC_API_KEY"]
ELEVENLABS_API_KEY  = os.environ["ELEVENLABS_API_KEY"]
ELEVENLABS_VOICE_ID = os.environ["ELEVENLABS_VOICE_ID"]
PEXELS_API_KEY      = os.environ["PEXELS_API_KEY"]

# YouTube credentials — file locally, JSON string in GitHub Actions
YOUTUBE_CREDENTIALS_FILE = "credentials.json"
YOUTUBE_TOKEN_FILE       = "token.json"
YOUTUBE_CREDENTIALS_JSON = os.environ.get("YOUTUBE_CREDENTIALS_JSON")

# Output directories
OUTPUT_DIR = "output"
AUDIO_DIR  = f"{OUTPUT_DIR}/audio"
CLIPS_DIR  = f"{OUTPUT_DIR}/clips"
VIDEOS_DIR = f"{OUTPUT_DIR}/videos"

# Pipeline settings
NICHE_KEYWORDS   = ["AI", "productivity", "personal finance", "tech"]  # edit for your niche
VIDEOS_PER_DAY   = 1
VIDEO_RESOLUTION = (1920, 1080)
VIDEO_FPS        = 30
