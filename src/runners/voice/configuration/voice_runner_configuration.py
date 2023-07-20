class VoiceRunnerConfiguration:
    
    def __init__(self, json_args):
        self.activation_cooldown = json_args["activation_cooldown"]
        self.save_audio = json_args.get("save_audio", False)
        self.wake_word_models = json_args["wake_word_models"]
        

    