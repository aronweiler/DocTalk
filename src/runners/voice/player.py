import pyaudio
import wave

import scipy.io.wavfile as wavfile
import numpy as np

def play_wav_file(file_path):
    chunk_size = 1024

    try:
        # Open the .wav file for reading
        wav_file = wave.open(file_path, 'rb')

        # Initialize PyAudio
        audio_player = pyaudio.PyAudio()

        # Open a stream to play the audio
        stream = audio_player.open(format=audio_player.get_format_from_width(wav_file.getsampwidth()),
                                   channels=wav_file.getnchannels(),
                                   rate=wav_file.getframerate(),
                                   output=True)

        # Read data in chunks and play it
        data = wav_file.readframes(chunk_size)
        while data:
            stream.write(data)
            data = wav_file.readframes(chunk_size)

        # Close the stream and PyAudio
        stream.stop_stream()
        stream.close()
        audio_player.terminate()

    except Exception as e:
        print("Error playing the .wav file:", str(e))

def _play_wav_file(filename, gain=1.0):
    chunk = 1024

    # Read the WAV file using scipy.io.wavfile
    sample_rate, audio_data = wavfile.read(filename)

    # Check if the audio data is in int16 format (common for WAV files)
    if audio_data.dtype == np.int16:
        # Convert the audio data to floating-point format for applying the gain
        audio_data = audio_data.astype(np.float32)

    # Apply the gain to the audio data
    scaled_audio_data = np.clip(gain * audio_data, -32767, 32767).astype(np.int16)

    # Initialize PyAudio
    p = pyaudio.PyAudio()

    # Open a stream
    stream = p.open(format=p.get_format_from_width(2),  # 2 bytes per sample for int16
                    channels=1,  # Mono audio
                    rate=sample_rate,
                    output=True)

    # Play the audio data
    idx = 0
    while idx < len(scaled_audio_data):
        stream.write(scaled_audio_data[idx:idx+chunk].tobytes())
        idx += chunk

    # Stop and close the stream
    stream.stop_stream()
    stream.close()

    # Terminate PyAudio
    p.terminate()

# Example usage:
# Replace 'your_file_path.wav' with the path to your .wav file and 'your_gain_value' with the desired gain value.
# play_wav_file('your_file_path.wav', your_gain_value)



def play_audio_stream(audio_stream, channels, sample_width, framerate):
    # Create an audio stream using PyAudio
    p = pyaudio.PyAudio()
    stream = p.open(format=p.get_format_from_width(sample_width),
                    channels=channels,
                    rate=framerate,
                    output=True)

    # Play the audio stream
    chunk_size = 1024
    data = audio_stream.read(chunk_size)
    while data:
        stream.write(data)
        data = audio_stream.read(chunk_size)

    # Stop and close the audio stream
    stream.stop_stream()
    stream.close()

    # Terminate the PyAudio object
    p.terminate()