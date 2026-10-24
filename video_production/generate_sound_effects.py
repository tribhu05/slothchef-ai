import os
import numpy as np
import wave

SAMPLE_RATE = 44100
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
AUDIO_DIR = os.path.join(SCRIPT_DIR, "assets", "audio")
os.makedirs(AUDIO_DIR, exist_ok=True)

def generate_chime(output_path=None):
    if output_path is None:
        output_path = os.path.join(AUDIO_DIR, "microwave_chime.wav")
        
    duration1 = 0.15
    duration2 = 0.55
    t1 = np.linspace(0, duration1, int(SAMPLE_RATE * duration1), endpoint=False)
    t2 = np.linspace(0, duration2, int(SAMPLE_RATE * duration2), endpoint=False)
    
    tone1 = 0.7 * np.sin(2 * np.pi * 587.33 * t1) + 0.2 * np.sin(2 * np.pi * 1174.66 * t1)
    sig1 = tone1 * np.exp(-3 * t1)
    
    tone2 = 0.8 * np.sin(2 * np.pi * 880.00 * t2) + 0.25 * np.sin(2 * np.pi * 1760.00 * t2)
    sig2 = tone2 * np.exp(-4 * t2)
    
    sig = np.concatenate([sig1, sig2])
    sig = sig / np.max(np.abs(sig)) * 0.85
    
    pcm = (np.clip(sig * 32767.0, -32767, 32767)).astype(np.int16)
    stereo = np.column_stack((pcm, pcm)).flatten()
    
    with wave.open(output_path, 'wb') as wav_file:
        wav_file.setnchannels(2)
        wav_file.setsampwidth(2)
        wav_file.setframerate(SAMPLE_RATE)
        wav_file.writeframes(stereo.tobytes())
    print(f"Chime generated: {output_path}")

def generate_ambient_track(total_seconds=170.0, output_path=None):
    if output_path is None:
        output_path = os.path.join(AUDIO_DIR, "ambient_track.wav")
        
    total_samples = int(SAMPLE_RATE * total_seconds)
    t = np.linspace(0, total_seconds, total_samples, endpoint=False)
    
    chords = [
        [130.81, 196.00, 246.94, 329.63], # Cmaj7
        [110.00, 164.81, 196.00, 261.63], # Am7
        [87.31, 130.81, 164.81, 220.00],  # Fmaj7
        [98.00, 146.83, 174.61, 246.94]   # G7
    ]
    chord_len = 4.0
    
    left = np.zeros(total_samples, dtype=np.float32)
    right = np.zeros(total_samples, dtype=np.float32)
    
    for i in range(int(total_seconds / chord_len) + 1):
        c_idx = i % len(chords)
        chord = chords[c_idx]
        start_idx = int(i * chord_len * SAMPLE_RATE)
        end_idx = min(int((i + 1) * chord_len * SAMPLE_RATE), total_samples)
        if start_idx >= total_samples:
            break
        n_samples = end_idx - start_idx
        chord_t = np.linspace(0, n_samples / SAMPLE_RATE, n_samples, endpoint=False)
        envelope = np.sin(np.pi * (chord_t / (chord_len + 0.5))) ** 2
        
        for freq in chord:
            pad_wave = 0.5 * np.sin(2 * np.pi * freq * chord_t) + 0.15 * np.sin(2 * np.pi * (freq * 2) * chord_t)
            left[start_idx:end_idx] += pad_wave * envelope * 0.12
            right[start_idx:end_idx] += pad_wave * envelope * 0.12
            
    sub_bass = 0.08 * np.sin(2 * np.pi * 55.0 * t) * (0.8 + 0.2 * np.sin(2 * np.pi * 0.25 * t))
    left += sub_bass
    right += sub_bass
    
    fade_in_len = int(1.5 * SAMPLE_RATE)
    fade_out_len = int(3.0 * SAMPLE_RATE)
    left[:fade_in_len] *= np.linspace(0, 1, fade_in_len)
    right[:fade_in_len] *= np.linspace(0, 1, fade_in_len)
    left[-fade_out_len:] *= np.linspace(1, 0, fade_out_len)
    right[-fade_out_len:] *= np.linspace(1, 0, fade_out_len)
    
    max_val = max(np.max(np.abs(left)), np.max(np.abs(right)))
    if max_val > 0:
        left = (left / max_val) * 0.35
        right = (right / max_val) * 0.35
        
    pcm_l = (np.clip(left * 32767.0, -32767, 32767)).astype(np.int16)
    pcm_r = (np.clip(right * 32767.0, -32767, 32767)).astype(np.int16)
    stereo = np.column_stack((pcm_l, pcm_r)).flatten()
    
    with wave.open(output_path, 'wb') as wav_file:
        wav_file.setnchannels(2)
        wav_file.setsampwidth(2)
        wav_file.setframerate(SAMPLE_RATE)
        wav_file.writeframes(stereo.tobytes())
    print(f"Ambient track generated: {output_path} ({total_seconds}s)")

if __name__ == '__main__':
    generate_chime()
    generate_ambient_track(170.0)
