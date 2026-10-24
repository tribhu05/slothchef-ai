import os
import wave
import numpy as np

SAMPLE_RATE = 48000
TOTAL_SECONDS = 170.0
TOTAL_SAMPLES = int(SAMPLE_RATE * TOTAL_SECONDS)

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
AUDIO_DIR = os.path.join(SCRIPT_DIR, "assets", "audio")

def read_wav_to_stereo(file_path, target_sr=48000):
    with wave.open(file_path, 'rb') as w:
        n_ch = w.getnchannels()
        sr = w.getframerate()
        n_frames = w.getnframes()
        data = w.readframes(n_frames)
        
    sig = np.frombuffer(data, dtype=np.int16).astype(np.float32) / 32768.0
    if n_ch == 2:
        sig = sig.reshape(-1, 2)
    else:
        sig = np.column_stack((sig, sig))
        
    if sr != target_sr:
        old_indices = np.linspace(0, len(sig) - 1, len(sig))
        new_len = int(len(sig) * target_sr / sr)
        new_indices = np.linspace(0, len(sig) - 1, new_len)
        resampled_l = np.interp(new_indices, old_indices, sig[:, 0])
        resampled_r = np.interp(new_indices, old_indices, sig[:, 1])
        sig = np.column_stack((resampled_l, resampled_r))
        
    return sig

def build_master_audio(output_path=None):
    if output_path is None:
        output_path = os.path.join(AUDIO_DIR, "master_audio.wav")
        
    master = np.zeros((TOTAL_SAMPLES, 2), dtype=np.float32)
    
    # 1. Add ambient track
    ambient_path = os.path.join(AUDIO_DIR, "ambient_track.wav")
    if os.path.exists(ambient_path):
        ambient = read_wav_to_stereo(ambient_path, SAMPLE_RATE)
        amb_len = min(len(ambient), TOTAL_SAMPLES)
        master[:amb_len] += ambient[:amb_len] * 0.22 # gentle background bed (-22dB)
        
    # 2. Add scene voiceovers
    voice_cues = [
        (os.path.join(AUDIO_DIR, "scene1_voice.wav"), 0.5),
        (os.path.join(AUDIO_DIR, "scene2_voice.wav"), 18.5),
        (os.path.join(AUDIO_DIR, "scene3_voice.wav"), 38.5),
        (os.path.join(AUDIO_DIR, "microwave_chime.wav"), 74.5), # Cooking timer chime
        (os.path.join(AUDIO_DIR, "scene4_voice.wav"), 83.5),
        (os.path.join(AUDIO_DIR, "scene5_voice.wav"), 118.5),
        (os.path.join(AUDIO_DIR, "scene6_voice.wav"), 143.5),
        (os.path.join(AUDIO_DIR, "scene7_voice.wav"), 162.2)
    ]
    
    for v_path, cue_sec in voice_cues:
        if os.path.exists(v_path):
            v_sig = read_wav_to_stereo(v_path, SAMPLE_RATE)
            start_idx = int(cue_sec * SAMPLE_RATE)
            end_idx = min(start_idx + len(v_sig), TOTAL_SAMPLES)
            add_len = end_idx - start_idx
            
            gain = 0.85 if "chime" in v_path else 1.05
            master[start_idx:end_idx] += v_sig[:add_len] * gain
            print(f"Added {os.path.basename(v_path)} at {cue_sec}s ({add_len/SAMPLE_RATE:.2f}s)")
            
    peak = np.max(np.abs(master))
    if peak > 0.95:
        master = master / peak * 0.95
        
    fade_out_samples = int(2.5 * SAMPLE_RATE)
    master[-fade_out_samples:] *= np.linspace(1, 0, fade_out_samples)[:, None]
    
    pcm = (np.clip(master * 32767.0, -32767, 32767)).astype(np.int16)
    with wave.open(output_path, 'wb') as wav_file:
        wav_file.setnchannels(2)
        wav_file.setsampwidth(2)
        wav_file.setframerate(SAMPLE_RATE)
        wav_file.writeframes(pcm.tobytes())
        
    print(f"Master audio successfully built: {output_path} ({TOTAL_SECONDS}s, 48kHz stereo)")

if __name__ == '__main__':
    build_master_audio()
