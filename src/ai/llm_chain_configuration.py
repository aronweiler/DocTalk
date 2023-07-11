class LLMChainConfiguration:
    
    def __init__(self, json_args):
        self.run_locally = json_args["run_locally"]
        self.ai_temp = json_args["ai_temp"]
        self.verbose = json_args["verbose"]
        self.max_tokens = json_args["max_tokens"]

    