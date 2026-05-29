# main.py
import os
from src.config import OUTPUT_DIR, AUDIO_DIR, CLIPS_DIR, VIDEOS_DIR
from src.scheduler import pop_next_topic
from src.script_gen import generate_script
from src.voiceover import generate_voiceover
from src.visuals import fetch_clips
from src.assembler import assemble_video
from src.metadata_gen import generate_metadata
from src.uploader import upload_to_youtube

def setup_dirs():
    for d in [OUTPUT_DIR, AUDIO_DIR, CLIPS_DIR, VIDEOS_DIR]:
        os.makedirs(d, exist_ok=True)

def run():
    setup_dirs()

    topic = pop_next_topic()
    if not topic:
        print("No topics in queue.")
        return

    print(f"Processing: {topic}")

    script        = generate_script(topic)
    audio_path    = generate_voiceover(script, AUDIO_DIR)
    clip_paths    = fetch_clips(script, CLIPS_DIR)
    video_path    = assemble_video(clip_paths, audio_path, VIDEOS_DIR)
    metadata      = generate_metadata(topic, script)
    video_id      = upload_to_youtube(video_path, metadata)

    print(f"Done. Live at: https://youtube.com/watch?v={video_id}")

if __name__ == "__main__":
    run()
