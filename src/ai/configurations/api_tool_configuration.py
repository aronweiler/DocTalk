class APIToolConfiguration:
    def __init__(self, json_args):
        self.run_locally = json_args["run_locally"]
        self.api_llm_model = json_args.get("model", None)
        self.ai_temp = json_args.get("api_temp", 0)
        self.api_llm_prompt = json_args.get("prompt", "###USER: {{query}}\n###ASSISTANT:\n")
    