import os
import subprocess
from src.config import VIDEOS_DIR, VIDEO_RESOLUTION, VIDEO_FPS


def assemble_video(
    clip_paths: list[str],
    audio_path: str,
    output_filename: str = "final.mp4",
) -> str:
    print("Assembling video...")
    os.makedirs(VIDEOS_DIR, exist_ok=True)
    output_path = os.path.join(VIDEOS_DIR, output_filename)

    # Get audio duration
    audio_duration = get_duration(audio_path)
    print(f"Audio duration: {audio_duration:.1f}s")

    # Build a looped/trimmed clip sequence that matches audio length
    clip_duration = audio_duration / len(clip_paths)
    processed_clips = []

    for i, clip_path in enumerate(clip_paths):
        processed = os.path.join(VIDEOS_DIR, f"proc_{i:02d}.mp4")
        w, h = VIDEO_RESOLUTION

        subprocess.run([
            "ffmpeg", "-y",
            "-i", clip_path,
            "-t", str(clip_duration),
            "-vf", f"scale={w}:{h}:force_original_aspect_ratio=increase,crop={w}:{h},setsar=1",
            "-r", str(VIDEO_FPS),
            "-c:v", "libx264",
            "-preset", "fast",
            "-an",
            processed,
        ], check=True, capture_output=True)

        processed_clips.append(processed)

    # Concatenate all clips
    concat_list_path = os.path.join(VIDEOS_DIR, "concat_list.txt")
    with open(concat_list_path, "w") as f:
        for p in processed_clips:
            f.write(f"file '{os.path.abspath(p)}'\n")

    silent_video = os.path.join(VIDEOS_DIR, "silent.mp4")
    subprocess.run([
        "ffmpeg", "-y",
        "-f", "concat",
        "-safe", "0",
        "-i", concat_list_path,
        "-c", "copy",
        silent_video,
    ], check=True, capture_output=True)

    # Merge audio + video
    subprocess.run([
        "ffmpeg", "-y",
        "-i", silent_video,
        "-i", audio_path,
        "-c:v", "copy",
        "-c:a", "aac",
        "-shortest",
        output_path,
    ], check=True, capture_output=True)

    # Cleanup temp files
    for p in processed_clips:
        os.remove(p)
    os.remove(silent_video)
    os.remove(concat_list_path)

    print(f"Video assembled: {output_path}")
    return output_path


def add_subtitles(video_path: str, audio_path: str) -> str:
    """
    Optional: generate and burn in subtitles using Whisper.
    Requires: pip install openai-whisper
    """
    try:
        import whisper
    except ImportError:
        print("Whisper not installed — skipping subtitles. Run: pip install openai-whisper")
        return video_path

    print("Generating subtitles with Whisper...")
    model = whisper.load_model("base")
    result = model.transcribe(audio_path)

    srt_path = video_path.replace(".mp4", ".srt")
    with open(srt_path, "w") as f:
        for i, seg in enumerate(result["segments"], 1):
            start = format_timestamp(seg["start"])
            end   = format_timestamp(seg["end"])
            f.write(f"{i}\n{start} --> {end}\n{seg['text'].strip()}\n\n")

    subtitled_path = video_path.replace(".mp4", "_subtitled.mp4")
    subprocess.run([
        "ffmpeg", "-y",
        "-i", video_path,
        "-vf", f"subtitles={srt_path}:force_style='FontSize=18,PrimaryColour=&HFFFFFF,OutlineColour=&H000000,Outline=2'",
        "-c:a", "copy",
        subtitled_path,
    ], check=True, capture_output=True)

    print(f"Subtitles burned in: {subtitled_path}")
    return subtitled_path


def get_duration(path: str) -> float:
    result = subprocess.run([
        "ffprobe", "-v", "error",
        "-show_entries", "format=duration",
        "-of", "default=noprint_wrappers=1:nokey=1",
        path,
    ], capture_output=True, text=True, check=True)
    return float(result.stdout.strip())


def format_timestamp(seconds: float) -> str:
    h = int(seconds // 3600)
    m = int((seconds % 3600) // 60)
    s = int(seconds % 60)
    ms = int((seconds % 1) * 1000)
    return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"

