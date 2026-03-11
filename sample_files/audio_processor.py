import os
import numpy as np
import librosa
import librosa.display
import matplotlib.pyplot as plt

AUDIO_FILE = 'sample.wav'

def load_audio(file_path):
    """Load an audio file using librosa."""
    try:
        y, sr = librosa.load(file_path)
        duration = librosa.get_duration(y=y, sr=sr)
        print(f"Loaded '{file_path}' | Duration: {duration:.2f} seconds")
        return y, sr
    except Exception as e:
        print(f"Error loading audio: {e}")
        return None, None

def plot_spectrogram(y, sr):
    """Generate and display a spectrogram of the audio signal."""
    spec = np.abs(librosa.stft(y))
    db_spec = librosa.amplitude_to_db(spec, ref=np.max)

    plt.figure(figsize=(10, 4))
    librosa.display.specshow(db_spec, sr=sr, x_axis='time', y_axis='log')
    plt.title("Spectrogram")
    plt.colorbar(format='%+2.0f dB')
    plt.tight_layout()
    plt.show()

def main():
    file_path = os.path.abspath(AUDIO_FILE)

    if not os.path.exists(file_path):
        print(f"Audio file not found: {file_path}")
        return

    y, sr = load_audio(file_path)
    if y is not None and sr is not None:
        plot_spectrogram(y, sr)

if __name__ == "__main__":
    main()
