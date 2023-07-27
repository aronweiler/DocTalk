import datetime
import os
import platform
import time
import threading
import numpy as np
import pyaudio
import queue
from collections import deque
import logging
import json

from ai.abstract_ai import AbstractAI
from ai.agent_tools.utilities.registered_settings import RegisteredSettings

from runners.runner import Runner
from runners.voice.configuration.voice_runner_configuration import (
    VoiceRunnerConfiguration,
    UserInformation,
    WakeWordModel,
)
from runners.voice.player import play_wav_file, play_wav_data
from runners.voice.sound import Sound
from runners.voice.prompts import VOICE_ASSISTANT_PROMPT
from runners.voice.audio_transcriber import AudioTranscriber
from runners.voice.wake_word import WakeWord
from runners.voice.text_to_speech import TextToSpeech

from memory.long_term.vector_database import VectorDatabase


from TTS.api import TTS

from dotenv import load_dotenv

if platform.system() == "Windows":
    import pyaudiowpatch as pyaudio

FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000
CHUNK = 1280
SILENCE_LIMIT_IN_SECONDS = 2

AI_USER_INFO = {"user_name": "Jarvis", "user_age": 0, "user_location": "The Void"}

class VoiceRunner(Runner):
    def __init__(self, args):
        super().__init__()
        self.args = VoiceRunnerConfiguration(args)
        self.audio = pyaudio.PyAudio()

        self.wake_word = WakeWord()

        self.activation_thread = None
        self.stop_event = threading.Event()
        self.audio_transcriber = AudioTranscriber(transcription_model_name=self.args.sts_model)

        # Create a queue to store audio frames
        self.audio_queue = queue.Queue(self.args.max_audio_queue_size)

        # initialize the text to speech engine
        self.text_to_speech = TextToSpeech()

        self.memory_db = VectorDatabase(self.args.db_env_location)        

    def configure(self, registered_settings: RegisteredSettings):
        # TODO: Add settings to control voice here
        pass

    def listen_to_microphone(self):
        # Set up the mic stream
        mic_stream = self.audio.open(
            format=FORMAT,
            channels=CHANNELS,
            rate=RATE,
            input=True,
        )

        while True:
            # If the wake word detection queue is full, pop the oldest frame
            if self.audio_queue.full():
                self.audio_queue.get()

            # Read a frame from the mic and add it to the queue used by the wake word detection
            frame = mic_stream.read(CHUNK, exception_on_overflow=False)
            self.audio_queue.put(frame, block=True)

            # Also put the frame into the audio transcriber
            self.audio_transcriber.add_frame_to_buffer(frame)

    def look_for_wake_words(self):
        # Set the last activation time to cooldown seconds ago so that we can activate immediately
        last_activation = time.time() - self.args.activation_cooldown

        # Start listening for wake words
        logging.info("\n\n--- Listening for wake words...\n")

        while True:
            # Pull a frame from the queue fed by the mic thread
            frame = self.audio_queue.get(block=True)

            # Predict whether a wake word is in this frame
            predictions = self.wake_word.get_wake_word_predictions(frame)

            # Get the highest ranked prediction (I only care about the best one)
            prediction = self.wake_word.get_highest_ranked_prediction(
                predictions, self.args.wake_word_models
            )

            # Does this prediction meet our threshold, and has enough time passed since the last activation?
            if (
                prediction is not None
                and prediction["prediction"][prediction["wake_word_model"]["model_name"]] > self.args.model_activation_threshold
                and (time.time() - last_activation) >= self.args.activation_cooldown
            ):
                detect_time = datetime.datetime.now().strftime("%Y_%m_%d_%H_%M_%S")

                logging.info(
                    f"Detected activation from '{prediction['wake_word_model']['model_name']}' model at time {detect_time}!  I think you are: {prediction['wake_word_model'].user_information.user_name}"
                )
                
                # Alert the user we've detected an activation
                play_wav_file(
                    os.path.join(
                        os.path.dirname(__file__), "audio", "activation.wav"
                    ),
                    self.stop_event,
                )

                # Detected an activation!  Let's process it on a different thread after stopping any other activations
                if self.activation_thread is not None:
                    self.stop_event.set()
                    self.audio_transcriber.stop_transcribing()
                    self.activation_thread.join()
                    self.activation_thread = None
                    self.stop_event.clear()                        

                self.activation_thread = threading.Thread(
                    target=self.process_activation, args=(prediction,)
                )
                self.activation_thread.start()

                last_activation = time.time()
                logging.debug("--- Continuing to listen for wake words...")


    def process_activation(self, prediction):
        # Mute any audio playing
        if self.args.mute_while_listening:
            Sound.mute()

        transcription_start_time = time.time()

        self.audio_transcriber.transcribe_until_silence(
            RATE, SILENCE_LIMIT_IN_SECONDS
        )

        transcribed_audio = self.audio_transcriber.get_transcription()

        if transcribed_audio is None or len(transcribed_audio) == 0:
            logging.info("No audio detected")
            # sad face
            self.text_to_speech.speak("I'm sorry, I didn't get that.  Can you please repeat your query?", prediction["wake_word_model"].tts_voice, self.stop_event)
            return

        # Create a memory
        # Might want to look at making this threaded to avoid blocking
        with self.memory_db.session_context(self.memory_db.Session()) as s:
            self.memory_db.add_conversation(
                s,
                prediction["wake_word_model"].user_information,
                transcribed_audio
            )

        transcription_end_time = time.time()

        logging.info(
            f"Transcription took {transcription_end_time - transcription_start_time} seconds"
        )

        # Alert the user we've stopped recording
        play_wav_file(
            os.path.join(
                os.path.dirname(__file__), "audio", "deactivate.wav"
            ),
            self.stop_event,
        )

        # Unmute the audio
        if self.args.mute_while_listening:
            Sound.volume_up()

        logging.info("Transcribed audio: " + transcribed_audio)

        if transcribed_audio is None or len(transcribed_audio) == 0:
            logging.debug("No audio detected")
            return

        if (
            transcribed_audio.strip().lower() == "stop"
            or transcribed_audio.strip().lower() == "stop."
            or transcribed_audio.strip().lower() == "cancel"
            or transcribed_audio.strip().lower() == "cancel."
        ):
            logging.debug("Stop keyword detected")
            return

        if self.stop_event.is_set():
            logging.debug("Stop event is set, cancelling interaction")
            return

        ai_query_start_time = time.time()

        ai_response = self.abstract_ai.query(
            self.get_prompt(
                transcribed_audio,
                prediction["wake_word_model"].user_information,
                prediction["wake_word_model"].personality_keywords,
            )
        )

        ai_query_end_time = time.time()
        logging.info(f"AI query took {str(ai_query_end_time - ai_query_start_time)} seconds")

        logging.debug("AI Response: " + ai_response.result_string)

        # Create a memory from the response
        # Might want to look at making this threaded to avoid blocking
        with self.memory_db.session_context(self.memory_db.Session()) as s:
            self.memory_db.add_conversation(
                s,
                AI_USER_INFO,
                ai_response.result_string
            )

        text_to_speech_start_time = time.time()
        self.text_to_speech.speak(ai_response.result_string, prediction["wake_word_model"].tts_voice, self.stop_event)
        text_to_speech_end_time = time.time()
        logging.info(f"Text to speech took {str(text_to_speech_end_time - text_to_speech_start_time)} seconds")        
        

    def run(self, abstract_ai: AbstractAI):
        self.abstract_ai = abstract_ai

        # Create the verifier models
        self.wake_word.create_verifier_models(self.args.wake_word_models)

        # Start the thread that listens to the microphone, putting data into the audio_queue
        mic_thread = threading.Thread(target=self.listen_to_microphone)
        mic_thread.start()

        # Start the thread that looks for wake words in the audio_queue
        wake_word_thread = threading.Thread(target=self.look_for_wake_words)
        wake_word_thread.start()

    def get_prompt(
        self, transcribed_audio, user_information:UserInformation, personality_keywords=None
    ):
        if personality_keywords is None:
            personality_keywords = ""

        user_info_string = f"Name: {user_information.user_name}, Age: {user_information.user_age}, Location: {user_information.user_location}, Email: {user_information.user_email}"
        
        prompt = VOICE_ASSISTANT_PROMPT.format(
            query=transcribed_audio,
            time_zone=datetime.datetime.now().astimezone().tzname(),
            current_date_time=datetime.datetime.now().strftime(
                "%I:%M %p %A, %B %d, %Y"
            ),
            user_information=user_info_string,
            personality_keywords=personality_keywords,
        )

        return prompt