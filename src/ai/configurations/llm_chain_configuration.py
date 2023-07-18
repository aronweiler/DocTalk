class LLMChainConfiguration:
    
    def __init__(self, json_args):
        self.run_locally = json_args["run_locally"]
        self.use_memory = json_args.get("use_memory", False)
        self.prompt = json_args.get("prompt", None)
        self.chat_model = json_args.get("chat_model", False)
        self.ai_temp = json_args.get("ai_temp", 0)
        self.verbose = json_args.get("verbose", False)
        self.max_tokens = json_args["max_tokens"]

    