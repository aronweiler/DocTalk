class VoiceRunnerConfiguration:
    
    def __init__(self, json_args):
        self.activation_cooldown = json_args["activation_cooldown"]
        self.mute_while_listening = json_args.get("mute_while_listening", False)
        self.save_audio = json_args.get("save_audio", False)
        self.wake_word_models = json_args["wake_word_models"]
        self.user_information = json_args["user_information"]
        

    