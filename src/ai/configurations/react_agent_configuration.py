class AgentWithToolsConfiguration:
    
    def __init__(self, json_args):
        # TODO: Implement this
        self.run_locally = json_args["run_locally"]
        self.use_memory = json_args["use_memory"]
        self.system_message = json_args.get("system_message", "")
        self.chat_model = json_args.get("chat_model", False)
        self.ai_temp = json_args["ai_temp"]
        self.verbose = json_args["verbose"]   
        self.max_tokens = json_args["max_tokens"]
        self.tools = json_args["tools"]

    