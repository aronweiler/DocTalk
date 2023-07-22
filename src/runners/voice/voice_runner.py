import datetime
import os
import platform
import time

from ai.abstract_ai import AbstractAI

from openwakeword.model import Model
from runners.runner import Runner
from runners.voice.configuration.voice_runner_configuration import VoiceRunnerConfiguration
from runners.voice.player import play_wav_file, play_audio_stream
from runners.voice.sound import Sound
from runners.voice.prompts import VOICE_ASSISTANT_PROMPT
from runners.voice.audio_transcriber import AudioTranscriber

import numpy as np

import wave


if platform.system() == "Windows":
    import pyaudiowpatch as pyaudio
else:
    import pyaudio


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
        self.audio_transcriber = AudioTranscriber()

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
                    if self.args.mute_while_listening:
                        Sound.mute()

                    # Stop the mic stream
                    mic_stream.stop_stream()

                    transcribed_audio = self.audio_transcriber.record_and_wait_for_silence(self.audio, FORMAT, CHANNELS, RATE, SILENCE_LIMIT_IN_SECONDS)

                    # Alert the user we've stopped recording
                    play_wav_file(os.path.join(os.path.dirname(__file__), 'audio', 'deactivate.wav'))

                    # Unmute the audio
                    if self.args.mute_while_listening:
                        Sound.volume_up()

                    try:
                        if transcribed_audio is None or len(transcribed_audio) == 0:
                            print("No audio detected")
                            continue                    

                        ai_response = abstract_ai.query(self.get_prompt(transcribed_audio))

                        print("AI Response: ", ai_response.result_string)

                        self.text_to_speech(ai_response.result_string)

                    finally: 
                        model.reset()                    
                        mic_stream.start_stream()
                        last_activation = time.time()                                      
                    
    def get_prompt(self, transcribed_audio):
        prompt = VOICE_ASSISTANT_PROMPT.format(query=transcribed_audio, 
                                               time_zone=datetime.datetime.now().astimezone().tzname(), 
                                               current_date_time=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                                               user_information=self.args.user_information)

        return prompt
    
    
    
    def init_voice(self):
        # Multi-speaker
        # model_name = "tts_models/en/vctk/fast_pitch"

        # Single speaker
        model_name = "tts_models/en/ljspeech/tacotron2-DCA"

        # Init TTS - should move this up so that it doesn't happen over and over
        self.tts = TTS(model_name=model_name, gpu=True)        

    def text_to_speech(self, text):
        # Might eventually stop saving things to file and just play them directly        
        file_path = os.path.join(os.path.dirname(__file__), 'output', 'tts_output.wav')

        # Some other voices
        #227 - 0
        #240 - 13
        #241 - 14        
        #250 - 23
        #260 - 33
        #270 - 43
        #278 - 51        

        if self.tts.speakers:
            self.tts.tts_to_file(text, speaker=self.tts.speakers[43], file_path=file_path)        
        else:
            self.tts.tts_to_file(text, file_path=file_path)        

        play_wav_file(file_path)

        # If file_path exists, delete it
        if os.path.exists(file_path):
            os.remove(file_path)