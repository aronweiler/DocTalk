import pyaudio
import wave

import scipy.io.wavfile as wavfile
import numpy as np


def play_wav_file(file_path, stop_event):
    chunk_size = 1024

    try:
        # Open the .wav file for reading
        wav_file = wave.open(file_path, "rb")

        # Initialize PyAudio
        audio_player = pyaudio.PyAudio()

        # Open a stream to play the audio
        stream = audio_player.open(
            format=audio_player.get_format_from_width(wav_file.getsampwidth()),
            channels=wav_file.getnchannels(),
            rate=wav_file.getframerate(),
            output=True,
        )

        # Read data in chunks and play it
        data = wav_file.readframes(chunk_size)
        while data and not stop_event.is_set():
            stream.write(data)
            data = wav_file.readframes(chunk_size)

        if stop_event.is_set():
            print("Stop event is set, cancelling audio playback.")

        # Close the stream and PyAudio
        stream.stop_stream()
        stream.close()
        audio_player.terminate()

    except Exception as e:
        print("Error playing the .wav file:", str(e))
