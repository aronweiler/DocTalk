class WakeWordModel:
    def __init__(self, json_args) -> None:
        self.model_name = json_args["model_name"]
        self.model_path = json_args["model_path"]
        self.training_data = json_args.get("training_data", None)
        self.user_information = json_args.get("user_information", None)
        self.personality_keywords = json_args.get("personality_keywords", "helpful, friendly")


class VoiceRunnerConfiguration:
    
    def __init__(self, json_args):
        self.activation_cooldown = json_args["activation_cooldown"]
        self.mute_while_listening = json_args.get("mute_while_listening", False)
        self.save_audio = json_args.get("save_audio", False)
        self.wake_word_models = self.get_wake_word_models(json_args.get("wake_word_models", {}))       
        
    def get_wake_word_models(self, json_args) -> list[WakeWordModel]:
        wake_word_models = []
        for wake_word_model in json_args:
            wake_word_models.append(WakeWordModel(wake_word_model))
        return wake_word_models

