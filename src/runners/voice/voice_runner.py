import datetime
import os
import platform
import time
import threading

from ai.abstract_ai import AbstractAI
from ai.agent_tools.utilities.registered_settings import RegisteredSettings

from openwakeword.model import Model
from runners.runner import Runner
from runners.voice.configuration.voice_runner_configuration import (
    VoiceRunnerConfiguration,
)
from runners.voice.player import play_wav_file
from runners.voice.sound import Sound
from runners.voice.prompts import VOICE_ASSISTANT_PROMPT
from runners.voice.audio_transcriber import AudioTranscriber


import numpy as np

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
        self.current_mic_audio_frames = []
        self.buffer_size = 20

    def configure(self, registered_settings: RegisteredSettings):
        # Register the buffer_size setting with in registered_settings
        registered_settings.register_setting("buffer_size", self.buffer_size)

    def run(self, abstract_ai: AbstractAI):
        self.audio = pyaudio.PyAudio()
        mic_stream = self.audio.open(
            format=FORMAT,
            channels=CHANNELS,
            rate=RATE,
            input=True,
            frames_per_buffer=CHUNK,
        )

        # initialize the speech system
        self.init_voice()

        # Can only have one custom verifier per model.  See https://github.com/dscripka/openWakeWord/issues/34
        # Create a model for each custom verifier in our wake word models configuration
        verifier_models = []
        for wake_word_model in self.args.wake_word_models:
            if wake_word_model.training_data is None:
                # No training data is available, create the model without the custom verifier
                model = Model(wakeword_models=[wake_word_model.model_path])
            else:
                # Training data is available, use a custom verifier
                model = Model(
                    wakeword_models=[wake_word_model.model_path],
                    custom_verifier_models={
                        wake_word_model.model_name: wake_word_model.training_data
                    },
                    custom_verifier_threshold=0.5,
                )

            verifier_models.append({"wake_word_model": wake_word_model, "model": model})

        # TODO: Remove in favor of sending to directly to AI
        output_dir = "./output"
        if not os.path.exists(output_dir):
            os.mkdir(output_dir)

        model_activation_threshold = 0.5

        # Predict continuously on audio stream
        last_activation = time.time()

        thread = None
        stop_event = threading.Event()

        print("\n\nListening for wakewords...\n")
        while True:
            # Get audio
            frame = mic_stream.read(CHUNK)
            current_mic_audio_frame = np.frombuffer(frame, dtype=np.int16)
            self.add_frame_to_buffer(current_mic_audio_frame)

            # Predict on each model
            predictions = []
            for model in verifier_models:
                predictions.append(
                    {
                        "prediction": model["model"].predict(current_mic_audio_frame),
                        "wake_word_model": model["wake_word_model"],
                    }
                )

            # # Try to clean up so we don't get follow-on activations
            # frame = None
            # current_mic_audio_frame = None

            # Get the highest ranked prediction (I only care about the best one)
            prediction = None
            for wake_word_model in self.args.wake_word_models:
                a_prediction = max(
                    predictions,
                    key=lambda item: item["prediction"][wake_word_model.model_name],
                )
                if (
                    prediction is None
                    or a_prediction["prediction"][wake_word_model.model_name]
                    > prediction["prediction"][wake_word_model.model_name]
                ):
                    prediction = a_prediction

            if prediction is None:
                continue

            # Check for model activations
            for mdl in prediction["prediction"].keys():
                # Does the activation meet our threshold, and has enough time passed since the last activation?
                if (
                    prediction["prediction"][mdl] > model_activation_threshold
                    and (time.time() - last_activation) >= self.args.activation_cooldown
                ):
                    detect_time = datetime.datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
                    print(
                        f'Detected activation from "{mdl}" model at time {detect_time}!'
                    )
                    print(
                        f"I think you are: {prediction['wake_word_model'].user_information}"
                    )

                    # Alert the user we've detected an activation
                    play_wav_file(
                        os.path.join(
                            os.path.dirname(__file__), "audio", "activation.wav"
                        ),
                        stop_event,
                    )

                    # Stop any running threads that are dealing with tasks
                    if thread is not None:
                        stop_event.set()
                        thread.join()
                        thread = None
                        stop_event.clear()

                    # Mute any audio playing
                    if self.args.mute_while_listening:
                        Sound.mute()

                    # Stop the mic stream
                    # mic_stream.stop_stream()

                    # Start the deal_with_it thread
                    thread = threading.Thread(
                        target=self.deal_with_it,
                        args=(
                            abstract_ai,
                            self.current_mic_audio_frames,
                            prediction,
                            stop_event,
                        ),
                    )
                    thread.start()

                    # print("Pausing for cooldown...")

                    # pause for the cooldown before starting the mic stream again
                    # time.sleep(self.args.activation_cooldown)

                    # mic_stream.start_stream()
                    last_activation = time.time()

                    print("Listening for wakewords...")

    def add_frame_to_buffer(self, frame):
        self.current_mic_audio_frames.append(frame)

        # If we've captured more than 10 frames, remove the first frame
        if len(self.current_mic_audio_frames) > self.buffer_size:
            self.current_mic_audio_frames.pop(0)

    def deal_with_it(
        self, abstract_ai: AbstractAI, current_mic_audio_frames, prediction, stop_event
    ):
        # TODO: Make this multi-threaded so that I can call the assistant again while it is speaking, and it will cancel its current interaction and start the new one
        audio_transcriber = AudioTranscriber()
        transcribed_audio = audio_transcriber.record_and_wait_for_silence(
            self.audio,
            current_mic_audio_frames,
            FORMAT,
            CHANNELS,
            RATE,
            SILENCE_LIMIT_IN_SECONDS,
        )

        # Alert the user we've stopped recording
        play_wav_file(
            os.path.join(os.path.dirname(__file__), "audio", "deactivate.wav"),
            stop_event,
        )

        # Unmute the audio
        if self.args.mute_while_listening:
            Sound.volume_up()

        print("Transcribed audio: ", transcribed_audio)

        if transcribed_audio is None or len(transcribed_audio) == 0:
            print("No audio detected")
            return

        if (
            transcribed_audio.strip().lower() == "stop"
            or transcribed_audio.strip().lower() == "stop."
            or transcribed_audio.strip().lower() == "cancel"
            or transcribed_audio.strip().lower() == "cancel."
        ):
            print("Stop keyword detected")
            return

        if stop_event.is_set():
            print("Stop event is set, cancelling interaction")
            return

        ai_response = abstract_ai.query(
            self.get_prompt(
                transcribed_audio,
                prediction["wake_word_model"].user_information,
                prediction["wake_word_model"].personality_keywords,
            )
        )

        print("AI Response: ", ai_response.result_string)

        self.text_to_speech(ai_response.result_string, stop_event)

    def get_prompt(
        self, transcribed_audio, user_information=None, personality_keywords=None
    ):
        if user_information is None:
            user_information = ""

        if personality_keywords is None:
            personality_keywords = ""

        prompt = VOICE_ASSISTANT_PROMPT.format(
            query=transcribed_audio,
            time_zone=datetime.datetime.now().astimezone().tzname(),
            current_date_time=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            user_information=user_information,
            personality_keywords=personality_keywords,
        )

        return prompt

    def init_voice(self):
        # Multi-speaker
        # model_name = "tts_models/en/vctk/fast_pitch"

        # Single speaker
        model_name = "tts_models/en/ljspeech/tacotron2-DCA"

        # Init TTS - should move this up so that it doesn't happen over and over
        self.tts = TTS(model_name=model_name, gpu=True)

    # Not the best TTS, but closer to real-time than anything else I've found right now
    def text_to_speech(self, text, stop_event):
        # Might eventually stop saving things to file and just play them directly
        file_path = os.path.join(os.path.dirname(__file__), "output", "tts_output.wav")

        # Some other voices
        # 227 - 0
        # 240 - 13
        # 241 - 14
        # 250 - 23
        # 260 - 33
        # 270 - 43
        # 278 - 51

        # Check to see if we've stopped before doing TTS
        if stop_event.is_set():
            print("Stop event is set, cancelling TTS")
            return

        if self.tts.speakers:
            self.tts.tts_to_file(
                text, speaker=self.tts.speakers[43], file_path=file_path
            )
        else:
            self.tts.tts_to_file(text, file_path=file_path)

        play_wav_file(file_path, stop_event)

        # If file_path exists, delete it
        if os.path.exists(file_path):
            os.remove(file_path)

    # https://github.com/suno-ai/bark/tree/main#-usage-in-python
    ## REALLY excellent TTS, but takes waaaayyyyy too long
    # from transformers import AutoProcessor, BarkModel
    # from IPython.display import Audio
    # from bark import SAMPLE_RATE, generate_audio, preload_models
    # from scipy.io.wavfile import write as write_wav
    # def text_to_speech(self, text):
    #     processor = AutoProcessor.from_pretrained("suno/bark")
    #     model = BarkModel.from_pretrained("suno/bark").to("cuda")

    #     voice_preset = "v2/en_speaker_6"

    #     inputs = processor(text, voice_preset=voice_preset)

    #     audio_array = model.generate(**inputs.to("cuda"))
    #     audio_array = audio_array.cpu().numpy().squeeze()

    #     file_path = os.path.join(os.path.dirname(__file__), 'output', 'tts_output.wav')
    #     write_wav(file_path, SAMPLE_RATE, audio_array)

    #     play_wav_file(file_path)

    #     # If file_path exists, delete it
    #     if os.path.exists(file_path):
    #         os.remove(file_path)
