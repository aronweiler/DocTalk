import threading
import webrtcvad
import torch
import queue
import numpy as np

class AudioTranscriber:

    def __init__(self):       
        import whisper   
        model_name = "base"
        device = ("cuda" if torch.cuda.is_available() else "cpu")
        self.model = whisper.load_model(model_name).to(device)

    def record_and_wait_for_silence(self, audio, format, channels, rate, silence_limit):        
        # Initialize WebRTC VAD
        vad = webrtcvad.Vad()
        # Aggressive VAD mode
        vad.set_mode(3)
        accumulated_silence = 0
        word_silence_limit = 0.5
        # Use a small chunk size to reduce latency and improve accuracy by looking for small chunks of silence, which would indicate a pause in speech
        chunk_size = 160

        # Set up the queue for the audio frames
        self.audio_queue = queue.Queue()
        # Set up a flag to indicate if the frames have been queued so that we don't start immediately queueing frames for transcription
        unqueued_frames = False

        # Start a thread to actively transcribe the incoming audio
        # This will significantly speed up the reaction times for the user
        thread = threading.Thread(target=self.transcribe_audio)

        # Start the transcription thread
        thread.start()

        # Create another mic input
        stream = audio.open(format=format,
                    channels=channels,
                    rate=rate,
                    input=True,
                    frames_per_buffer=chunk_size)
        frames = []

        try:
            
            while True:                
                frame = stream.read(chunk_size, exception_on_overflow=False)

                # Convert the frame to an array and append it to the frames list
                frame_array = torch.from_numpy(np.frombuffer(frame, np.int16).flatten().astype(np.float32) / 32768.0)
                frames.append(frame_array)

                # Check if the frame is speech or not
                is_speech = vad.is_speech(frame, sample_rate=rate)

                # TODO: Look at speeding this up by removing silences from the transcription queue

                if is_speech:
                    # Reset the silence threshold
                    accumulated_silence = 0
                    
                    # We got some speech, so the next silence we should flag ourselves so that we queue the frames
                    unqueued_frames = True

                elif not is_speech:
                    # If this is a silent frame, we should add the previous frames to the transcription queue
                    # Also check to see if the silence limit has been hit for the word silence limit
                    # Only do this if we haven't already queued the frames
                    
                    if unqueued_frames and accumulated_silence >= word_silence_limit * (rate / chunk_size):
                        # Concatenate the frames
                        joined_frames = np.concatenate(frames)
                        #torch_audio = torch.from_numpy(np.frombuffer(audio.get_raw_data(), np.int16).flatten().astype(np.float32) / 32768.0)
                        self.audio_queue.put(joined_frames)
                        unqueued_frames = False

                        print(f"Queuing {len(frames)} frames")

                        # Clear the frames, because now they are queued
                        frames = []

                    # Also, if there is no speech in the frame, increment the silence threshold and continue listening
                    if accumulated_silence < silence_limit * (rate / chunk_size):                        
                        accumulated_silence += 1
                        continue
                    else:
                        # Or, if the silence threshold is met, stop listening 
                        print("Silence threshold met, accumulated_silence=", accumulated_silence)                        

                        # Stop the transcription thread
                        self.audio_queue.put(None)
                        break
        finally:
            stream.stop_stream()
            stream.close()
            
        # Join on the transcription thread
        thread.join()

        # Return the transcribed audio
        return self.transcribed_audio

    # This call requires ffmpeg!!
    def transcribe_audio(self):
        transcription = ''

        running_frames = []

        # Continuously transcribe the audio from the queue, when None is received, stop
        while True:
            dequeued_item = self.audio_queue.get()           

            # The calling thread is cancelling this
            if dequeued_item is None:
                break

            # Append the dequeued frame to the running frames
            running_frames.append(dequeued_item)

            print(f"Transcribing {len(running_frames[0]) / 16000} seconds of audio")
         
            # Attempt to transcribe the chunk of audio
            # Note, this includes the previously unsuccessfully transcribed frames (if any)
            result = self.model.transcribe(audio=np.concatenate(running_frames))

            result_text = result["text"]
            print("Transcribed: ", result_text)

            # If result text is not empty, add it to the transcription and reset the running frames
            if result_text != '':
                transcription += result_text
                running_frames = []

        self.transcribed_audio = transcription
