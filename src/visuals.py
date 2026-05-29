import os
import requests
from src.config import PEXELS_API_KEY, CLIPS_DIR


PEXELS_VIDEO_URL = "https://api.pexels.com/videos/search"
HEADERS = {"Authorization": PEXELS_API_KEY}


def search_pexels_video(keyword: str, per_page: int = 3) -> list[dict]:
    params = {
        "query": keyword,
        "per_page": per_page,
        "orientation": "landscape",
        "size": "large",
    }
    response = requests.get(PEXELS_VIDEO_URL, headers=HEADERS, params=params, timeout=30)

    if response.status_code != 200:
        print(f"Pexels search failed for '{keyword}': {response.status_code}")
        return []

    videos = response.json().get("videos", [])
    return videos


def get_best_video_file(video: dict, min_width: int = 1920) -> str | None:
    files = sorted(
        video.get("video_files", []),
        key=lambda f: f.get("width", 0),
        reverse=True,
    )
    for f in files:
        if f.get("width", 0) >= min_width and f.get("file_type") == "video/mp4":
            return f["link"]
    # fallback to highest resolution available
    if files:
        return files[0]["link"]
    return None


def download_clip(url: str, filename: str) -> str:
    os.makedirs(CLIPS_DIR, exist_ok=True)
    output_path = os.path.join(CLIPS_DIR, filename)

    if os.path.exists(output_path):
        print(f"Clip already exists, skipping: {filename}")
        return output_path

    response = requests.get(url, stream=True, timeout=60)
    response.raise_for_status()

    with open(output_path, "wb") as f:
        for chunk in response.iter_content(chunk_size=1024 * 1024):
            f.write(chunk)

    print(f"Downloaded clip: {filename}")
    return output_path


def fetch_clips(keywords: list[str], num_clips: int = 6) -> list[str]:
    print(f"Fetching {num_clips} clips from Pexels...")
    clip_paths = []

    for i, keyword in enumerate(keywords):
        if len(clip_paths) >= num_clips:
            break

        videos = search_pexels_video(keyword, per_page=2)

        for video in videos:
            if len(clip_paths) >= num_clips:
                break

            file_url = get_best_video_file(video)
            if not file_url:
                continue

            filename = f"clip_{i:02d}_{video['id']}.mp4"
            try:
                path = download_clip(file_url, filename)
                clip_paths.append(path)
            except Exception as e:
                print(f"Failed to download clip for '{keyword}': {e}")

    if not clip_paths:
        raise RuntimeError("No clips downloaded — check your Pexels API key and keywords.")

    print(f"Fetched {len(clip_paths)} clips total.")
    return clip_paths

