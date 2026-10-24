import os
import sys
import subprocess
import shutil

# Locate high-performance FFmpeg 7.1 binary
FFMPEG_PATHS = [
    r"C:\Python314\Lib\site-packages\imageio_ffmpeg\binaries\ffmpeg-win-x86_64-v7.1.exe",
    shutil.which("ffmpeg")
]
FFMPEG_BIN = None
for p in FFMPEG_PATHS:
    if p and os.path.exists(p):
        FFMPEG_BIN = p
        break

if not FFMPEG_BIN:
    raise RuntimeError("FFmpeg binary not found. Please install ffmpeg or imageio-ffmpeg.")

print(f"Using FFmpeg: {FFMPEG_BIN}")

WORKDIR = os.path.dirname(os.path.abspath(__file__))
ASSETS_DIR = os.path.join(WORKDIR, "assets")
FOOTAGE_DIR = os.path.join(ASSETS_DIR, "footage")
CARDS_DIR = os.path.join(ASSETS_DIR, "cards")
AUDIO_DIR = os.path.join(ASSETS_DIR, "audio")
TEMP_CLIPS_DIR = os.path.join(WORKDIR, "temp_clips")
os.makedirs(TEMP_CLIPS_DIR, exist_ok=True)

MASTER_AUDIO = os.path.join(AUDIO_DIR, "master_audio.wav")
FINAL_OUTPUT = os.path.join(WORKDIR, "slothchef-demo.mp4")
CAPTIONS_FILE = os.path.join(WORKDIR, "captions.srt")

# Target scene segments: exactly 170.0s (2:50) at 30fps
SCENE_SEGMENTS = [
    # Scene 1: The Midnight Crisis (18.0s)
    {
        "id": "clip1_midnight_crisis",
        "type": "image",
        "src": os.path.join(CARDS_DIR, "card_scene1_hook.png"),
        "duration": 18.0
    },
    # Scene 2: Meet SlothChef (20.0s total: 10s contract + 10s live UI)
    {
        "id": "clip2a_sloth_contract",
        "type": "image",
        "src": os.path.join(CARDS_DIR, "card_scene2_sloth_contract.png"),
        "duration": 10.0
    },
    {
        "id": "clip2b_live_homepage",
        "type": "image",
        "src": os.path.join(FOOTAGE_DIR, "shot_live_loaded.png"),
        "duration": 10.0
    },
    # Scene 3: The Real Product Demo (45.0s total: 34s live recording + 8s cook-along + 3s tabpfn radar)
    {
        "id": "clip3a_live_recording",
        "type": "video",
        "src": os.path.join(FOOTAGE_DIR, "live_demo_raw.webm"),
        "duration": 34.0
    },
    {
        "id": "clip3b_cook_along",
        "type": "image",
        "src": os.path.join(FOOTAGE_DIR, "shot_cook_along.png"),
        "duration": 8.0
    },
    {
        "id": "clip3c_tabpfn_radar",
        "type": "image",
        "src": os.path.join(FOOTAGE_DIR, "shot_tabpfn_modal.png"),
        "duration": 3.0
    },
    # Scene 4: How It Works - Dual AI Architecture (35.0s)
    {
        "id": "clip4_architecture",
        "type": "image",
        "src": os.path.join(CARDS_DIR, "card_scene4_architecture.png"),
        "duration": 35.0
    },
    # Scene 5: Open Innovation & Render Deployment (25.0s)
    {
        "id": "clip5_deployment",
        "type": "image",
        "src": os.path.join(CARDS_DIR, "card_scene5_deployment.png"),
        "duration": 25.0
    },
    # Scene 6: The Payoff (19.0s)
    {
        "id": "clip6_payoff",
        "type": "image",
        "src": os.path.join(CARDS_DIR, "card_scene6_payoff.png"),
        "duration": 19.0
    },
    # Scene 7: Closing End Card (8.0s)
    {
        "id": "clip7_endcard",
        "type": "image",
        "src": os.path.join(CARDS_DIR, "card_scene7_endcard.png"),
        "duration": 8.0
    }
]

def render_segment(seg):
    out_path = os.path.join(TEMP_CLIPS_DIR, f"{seg['id']}.mp4")
    dur = seg['duration']
    
    if seg['type'] == 'image':
        cmd = [
            FFMPEG_BIN, "-y",
            "-loop", "1",
            "-t", str(dur),
            "-i", seg['src'],
            "-vf", "scale=1920:1080:force_original_aspect_ratio=decrease,pad=1920:1080:(ow-iw)/2:(oh-ih)/2,format=yuv420p",
            "-r", "30",
            "-c:v", "libx264",
            "-preset", "faster",
            "-crf", "18",
            out_path
        ]
    else: # Video
        cmd = [
            FFMPEG_BIN, "-y",
            "-ss", "0",
            "-t", str(dur),
            "-i", seg['src'],
            "-vf", "scale=1920:1080:force_original_aspect_ratio=decrease,pad=1920:1080:(ow-iw)/2:(oh-ih)/2,format=yuv420p",
            "-r", "30",
            "-c:v", "libx264",
            "-preset", "faster",
            "-crf", "18",
            out_path
        ]
        
    print(f"Rendering segment: {seg['id']} ({dur}s)...")
    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode != 0:
        print(f"Error rendering {seg['id']}:", res.stderr)
        raise RuntimeError(f"FFmpeg failed for {seg['id']}")
    print(f"Segment done: {out_path}")
    return out_path

def assemble_final_video():
    clip_paths = []
    total_time = 0.0
    for seg in SCENE_SEGMENTS:
        p = render_segment(seg)
        clip_paths.append(p)
        total_time += seg['duration']
        
    print(f"All segments rendered! Total video timeline: {total_time:.2f}s")
    
    # Write concat list
    concat_list_file = os.path.join(TEMP_CLIPS_DIR, "concat_list.txt")
    with open(concat_list_file, "w", encoding="utf-8") as f:
        for cp in clip_paths:
            # Escape path for FFmpeg concat
            norm_p = cp.replace("\\", "/")
            f.write(f"file '{norm_p}'\n")
            
    temp_concat_video = os.path.join(TEMP_CLIPS_DIR, "temp_full_video.mp4")
    concat_cmd = [
        FFMPEG_BIN, "-y",
        "-f", "concat",
        "-safe", "0",
        "-i", concat_list_file,
        "-c", "copy",
        temp_concat_video
    ]
    print("Concatenating video segments...")
    res = subprocess.run(concat_cmd, capture_output=True, text=True)
    if res.returncode != 0:
        print("Concat error:", res.stderr)
        raise RuntimeError("Concat failed")
        
    # Multiplex with master_audio.wav and embed captions.srt
    print("Multiplexing video with master audio and subtitle tracks...")
    
    mux_cmd = [
        FFMPEG_BIN, "-y",
        "-i", temp_concat_video,
        "-i", MASTER_AUDIO,
        "-i", CAPTIONS_FILE,
        "-map", "0:v:0",
        "-map", "1:a:0",
        "-map", "2:s:0?",
        "-c:v", "copy",
        "-c:a", "aac",
        "-b:a", "192k",
        "-c:s", "mov_text",
        "-metadata:s:s:0", "language=eng",
        "-metadata:s:s:0", "title=English",
        "-shortest",
        FINAL_OUTPUT
    ]
    
    res = subprocess.run(mux_cmd, capture_output=True, text=True)
    if res.returncode != 0:
        # Fallback without subtitle track if mov_text fails
        print("Muxing without subtitle stream fallback...")
        mux_cmd_no_sub = [
            FFMPEG_BIN, "-y",
            "-i", temp_concat_video,
            "-i", MASTER_AUDIO,
            "-map", "0:v:0",
            "-map", "1:a:0",
            "-c:v", "copy",
            "-c:a", "aac",
            "-b:a", "192k",
            "-shortest",
            FINAL_OUTPUT
        ]
        res2 = subprocess.run(mux_cmd_no_sub, capture_output=True, text=True)
        if res2.returncode != 0:
            print("Mux error:", res2.stderr)
            raise RuntimeError("Multiplexing failed")
            
    print(f"\n==========================================")
    print(f"SUCCESS: SlothChef Demo Video Rendered!")
    print(f"Output File: {FINAL_OUTPUT}")
    file_size_mb = os.path.getsize(FINAL_OUTPUT) / (1024 * 1024)
    print(f"File Size: {file_size_mb:.2f} MB")
    print(f"==========================================")

if __name__ == '__main__':
    assemble_final_video()
