import collections
from collections import deque
import datetime
import os
import platform
import time

from ai.abstract_ai import AbstractAI

from openwakeword.model import Model
from queue import Queue
from runners.runner import Runner
from runners.voice.configuration.voice_runner_configuration import VoiceRunnerConfiguration
from runners.voice.player import play_wav_file, play_audio_stream
from runners.voice.sound import Sound
from runners.voice.prompts import VOICE_ASSISTANT_PROMPT

from transformers import SpeechT5Processor, SpeechT5ForTextToSpeech, SpeechT5HifiGan
from datasets import load_dataset
import torch
import soundfile as sf
from datasets import load_dataset

import numpy as np
import torch
import wave
import webrtcvad

if platform.system() == "Windows":
    import pyaudiowpatch as pyaudio
else:
    import pyaudio

import whisper  
from TTS.api import TTS

FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000
CHUNK = 1280
SILENCE_LIMIT_IN_SECONDS = 2

class VoiceRunner(Runner):
    def __init__(self, args):
        super().__init__()
        self.args = VoiceRunnerConfiguration(args)

    def run(self, abstract_ai: AbstractAI):    
        self.audio = pyaudio.PyAudio()
        mic_stream = self.audio.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK)        

        # initialize the speech system
        self.init_voice()

        # Instantiate the model
        model = Model(
            wakeword_models=self.args.wake_word_models,
        )

        # TODO: Remove in favor of sending to AI
        output_dir = "./output"        
        if not os.path.exists(output_dir):
            os.mkdir(output_dir)

        model_activation_threshold = 0.5        

        # Predict continuously on audio stream
        last_activation = time.time()

        #circular_buffer = Queue(maxsize=50)

        print("\n\nListening for wakewords...\n")
        while True:            
            # Get audio
            frame = mic_stream.read(CHUNK)            
            #self.enqueue_with_overflow(circular_buffer, frame)
            mic_audio = np.frombuffer(frame, dtype=np.int16)                           

            # Feed to openWakeWord model
            prediction = model.predict(mic_audio)

            # Try to clean up so we don't get follow-on activations
            frame = None
            mic_audio = None

            # Check for model activations (score above threshold), and save clips
            for mdl in prediction.keys():                
                # Does the activation meet our threshold, and has enough time passed since the last activation?
                if prediction[mdl] > model_activation_threshold and (time.time() - last_activation) >= self.args.activation_cooldown:
                    
                    detect_time = datetime.datetime.now().strftime("%Y_%m_%d_%H_%M_%S")                    
                    print(f'Detected activation from \"{mdl}\" model at time {detect_time}!')

                    # Alert the user we've detected an activation
                    play_wav_file(os.path.join(os.path.dirname(__file__), 'audio', 'activation.wav'))

                    # Mute any audio playing
                    Sound.mute()

                    # Stop the stream
                    mic_stream.stop_stream()

                    frames = self.record_and_wait_for_silence()

                    # Unmute the audio
                    Sound.volume_up()                                     

                    temp_file_name = detect_time + f"_{mdl}.wav"
                    
                    print(f"Saving audio to {temp_file_name}")

                    output_file = os.path.join(os.path.abspath(output_dir), temp_file_name)
                    wf = wave.open(output_file, 'wb')
                    wf.setnchannels(CHANNELS)
                    wf.setsampwidth(self.audio.get_sample_size(FORMAT))
                    wf.setframerate(RATE)
                    wf.writeframes(b''.join(frames))
                    wf.close()

                    # Alert the user we've stopped recording
                    play_wav_file(os.path.join(os.path.dirname(__file__), 'audio', 'deactivate.wav'))

                    transcribed_audio = self.transcribe_audio(audio_file=output_file)
                    
                    ai_response = abstract_ai.query(self.get_prompt(transcribed_audio))

                    print("AI Response: ", ai_response.result_string)

                    self.text_to_speech(ai_response.result_string)

                    if self.args.save_audio != True:
                        # Remove the file
                        os.remove(output_file)

                    model.reset()                    
                    mic_stream.start_stream()

                    last_activation = time.time()                                      
                    
    def get_prompt(self, transcribed_audio):
        prompt = VOICE_ASSISTANT_PROMPT.format(query=transcribed_audio, 
                                               time_zone=datetime.datetime.now().astimezone().tzname(), 
                                               current_date_time=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

        return prompt

    def enqueue_with_overflow(self, fifo_queue, element):
        if fifo_queue.full():
            fifo_queue.get()  # Discard the first element
        fifo_queue.put(element)
    
    def record_and_wait_for_silence(self):        
        # Initialize WebRTC VAD
        vad = webrtcvad.Vad()
        # Aggressive VAD mode
        vad.set_mode(3)
        silence_threshold = 0
        silence_chunk = 160
        frames = []

        # Create another mic input
        stream = self.audio.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=silence_chunk)
        try:
        
            while True:
                # Tells me if there is speech in this frame            
                #frame = mic_stream.read(CHUNK)
                frame = stream.read(silence_chunk)
                frames.append(frame)

                is_speech = vad.is_speech(frame, sample_rate=RATE)  

                if is_speech:
                    print("SPEECH")
                    # Reset the silence threshold
                    silence_threshold = 0
                elif not is_speech:
                    # if no speech is detected but script was expecting speech
                    # check if the silence_threshold is less than 4 seconds
                    # if it is, increase the silence_threshold of 10ms
                    # otherwise 4 seconds have passed and the user stopped speaking
                    # so we can proceed to process the buffer in waveform and reset
                    if silence_threshold < SILENCE_LIMIT_IN_SECONDS * (RATE / silence_chunk):
                        silence_threshold += 1
                        print("silence_threshold=", silence_threshold)
                        continue
                    else:
                        print("Silence Detected, silence_threshold=", silence_threshold)                        
                        return frames
        finally:
            stream.stop_stream()
            stream.close()     

    def transcribe_audio(self, audio_file, model_name = "base", device = ("cuda" if torch.cuda.is_available() else "cpu")):
        model = whisper.load_model(model_name).to(device)

        # This call requires ffmpeg!!
        result = model.transcribe(audio=audio_file)
        print("Transcribed: ", result["text"])
        return result["text"]
    
    def init_voice(self):
        # Multi-speaker
        # model_name = "tts_models/en/vctk/fast_pitch"

        # Single speaker
        model_name = "tts_models/en/ljspeech/tacotron2-DCA"

        # Init TTS - should move this up so that it doesn't happen over and over
        self.tts = TTS(model_name=model_name, gpu=True)        

    def text_to_speech(self, text):
        # Might eventually stop saving things to file and just play them directly        
        file_path = os.path.join(os.path.dirname(__file__), 'output', 'hello_world.wav')

        # Some other voices
        #227 - 0
        #240 - 13
        #241 - 14        
        #250 - 23
        #260 - 33
        #270 - 43
        #278 - 51        

        if self.tts.speakers:
            self.tts.tts_to_file(text, speaker=self.tts.speakers[23], file_path=file_path)        
        else:
            self.tts.tts_to_file(text, file_path=file_path)        

        play_wav_file(file_path)

        # If file_path exists, delete it
        if os.path.exists(file_path):
            os.remove(file_path)            

    # def init_voice(self):  
    #     self.processor = SpeechT5Processor.from_pretrained("microsoft/speecht5_tts")
    #     self.model = SpeechT5ForTextToSpeech.from_pretrained("microsoft/speecht5_tts")
    #     self.vocoder = SpeechT5HifiGan.from_pretrained("microsoft/speecht5_hifigan")

    #     # load xvector containing speaker's voice characteristics from a dataset
    #     embeddings_dataset = load_dataset("Matthijs/cmu-arctic-xvectors", split="validation")
    #     self.speaker_embeddings = torch.tensor(embeddings_dataset[7306]["xvector"]).unsqueeze(0)


    # def text_to_speech(self, text):
    #     inputs = self.processor(text=text, return_tensors="pt")

    #     speech = self.model.generate_speech(inputs["input_ids"], self.speaker_embeddings, vocoder=self.vocoder)

    #     file_path = os.path.join(os.path.dirname(__file__), 'output', 'hello_world.wav')

    #     sf.write(file_path, speech.numpy(), samplerate=RATE)

    #     play_wav_file(file_path, gain=6)