class QAChainConfiguration:
    
    def __init__(self, json_args):
        self.run_locally = json_args["run_locally"]
        self.use_memory = json_args["use_memory"]
        self.ai_temp = json_args["ai_temp"]
        self.database_name = json_args["database_name"]
        self.top_k = json_args["top_k"]
        self.search_type = json_args["search_type"]
        self.search_distance = json_args["search_distance"]
        self.verbose = json_args["verbose"]
        self.max_tokens = json_args["max_tokens"]
        self.return_source_documents = json_args["return_source_documents"]
        self.return_direct = json_args["return_direct"]
        self.chain_type = json_args["chain_type"]

    