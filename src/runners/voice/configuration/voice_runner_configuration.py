class VoiceRunnerConfiguration:
    
    def __init__(self, json_args):
        self.save_audio = json_args.get("save_audio", False)
        self.wake_word_models = json_args["wake_word_models"]
        

    