import pyaudio
import wave
import logging

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
            logging.debug("Stop event is set, cancelling audio playback.")

        # Close the stream and PyAudio
        stream.stop_stream()
        stream.close()
        audio_player.terminate()

    except Exception as e:
        logging.debug("Error playing the .wav file:" + str(e))


def play_wav_data(wav_data, stop_event, sample_rate=16000, sample_width=2, channels=1):
    chunk_size = 1024

    try:
        # Initialize PyAudio
        audio_player = pyaudio.PyAudio()

        # Open a stream to play the audio
        stream = audio_player.open(
            format=audio_player.get_format_from_width(sample_width),
            channels=channels,
            rate=sample_rate,
            output=True,
        )

        # Read data in chunks and play it
        index = 0
        data = wav_data[index:chunk_size]
        while data and not stop_event.is_set():
            stream.write(data)
            data = wav_data[index:chunk_size]
            index += chunk_size

        if stop_event.is_set():
            logging.debug("Stop event is set, cancelling audio playback.")

        # Close the stream and PyAudio
        stream.stop_stream()
        stream.close()
        audio_player.terminate()

    except Exception as e:
        logging.debug("Error playing the wav data:" + str(e))
