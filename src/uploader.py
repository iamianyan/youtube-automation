import os
import json
import tempfile
from src.config import (
    YOUTUBE_CREDENTIALS_FILE,
    YOUTUBE_TOKEN_FILE,
    YOUTUBE_CREDENTIALS_JSON,
)

from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

SCOPES = ["https://www.googleapis.com/auth/youtube.upload"]


def get_youtube_client():
    creds = None

    # Load existing token
    if os.path.exists(YOUTUBE_TOKEN_FILE):
        creds = Credentials.from_authorized_user_file(YOUTUBE_TOKEN_FILE, SCOPES)

    # Refresh if expired
    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
        _save_token(creds)

    # First-time auth — runs locally only
    if not creds or not creds.valid:
        if YOUTUBE_CREDENTIALS_JSON:
            # GitHub Actions: credentials stored as env var JSON string
            with tempfile.NamedTemporaryFile(
                mode="w", suffix=".json", delete=False
            ) as tmp:
                tmp.write(YOUTUBE_CREDENTIALS_JSON)
                tmp_path = tmp.name
            flow = InstalledAppFlow.from_client_secrets_file(tmp_path, SCOPES)
            os.unlink(tmp_path)
        elif os.path.exists(YOUTUBE_CREDENTIALS_FILE):
            # Local: credentials.json file
            flow = InstalledAppFlow.from_client_secrets_file(
                YOUTUBE_CREDENTIALS_FILE, SCOPES
            )
        else:
            raise FileNotFoundError(
                "No YouTube credentials found. "
                "Set YOUTUBE_CREDENTIALS_JSON env var or provide credentials.json"
            )

        creds = flow.run_local_server(port=0)
        _save_token(creds)

    return build("youtube", "v3", credentials=creds)


def _save_token(creds: Credentials):
    with open(YOUTUBE_TOKEN_FILE, "w") as f:
        f.write(creds.to_json())


def upload_to_youtube(
    video_path: str,
    metadata: dict,
    privacy: str = "public",
) -> str:
    print("Uploading to YouTube...")
    youtube = get_youtube_client()

    body = {
        "snippet": {
            "title":       metadata["title"],
            "description": metadata["description"],
            "tags":        metadata.get("tags", []),
            "categoryId":  metadata.get("category_id", "22"),
        },
        "status": {
            "privacyStatus":          privacy,
            "selfDeclaredMadeForKids": False,
        },
    }

    media = MediaFileUpload(
        video_path,
        mimetype="video/mp4",
        resumable=True,
        chunksize=1024 * 1024 * 10,  # 10MB chunks
    )

    request = youtube.videos().insert(
        part="snippet,status",
        body=body,
        media_body=media,
    )

    response = None
    while response is None:
        status, response = request.next_chunk()
        if status:
            pct = int(status.progress() * 100)
            print(f"Upload progress: {pct}%")

    video_id = response["id"]
    print(f"Uploaded: https://youtube.com/watch?v={video_id}")
    return video_id
