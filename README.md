# YouTube Automation Pipeline

Automated faceless YouTube video pipeline — generates scripts with Claude AI,
narrates with ElevenLabs, assembles video with FFmpeg, and uploads to YouTube
on a daily schedule via GitHub Actions.

## How it works

1. Topic scheduler pulls trending topics (Google Trends / RSS / manual queue)
2. Claude API writes a structured script (hook, body, CTA)
3. ElevenLabs generates a voiceover MP3
4. Pexels fetches relevant stock footage
5. FFmpeg assembles the final video with captions
6. YouTube Data API v3 uploads and schedules the video

## Setup

### Prerequisites
- Python 3.11+
- FFmpeg installed locally
- API keys for: Anthropic, ElevenLabs, Pexels, YouTube Data API

### Installation

git clone https://github.com/YOUR_USERNAME/youtube-automation.git
cd youtube-automation
pip install -r requirements.txt
cp .env.example .env   # fill in your keys

### Running locally

python main.py

### GitHub Actions (automated daily)

Add your API keys as repository secrets (Settings → Secrets → Actions),
then push to main. The workflow triggers daily at midnight UTC.

## Environment variables

| Variable | Description |
|---|---|
| ANTHROPIC_API_KEY | Claude API key |
| ELEVENLABS_API_KEY | ElevenLabs API key |
| ELEVENLABS_VOICE_ID | Your ElevenLabs voice ID |
| PEXELS_API_KEY | Pexels API key |
| YOUTUBE_CREDENTIALS_JSON | YouTube OAuth credentials (JSON) |

## License

MIT
