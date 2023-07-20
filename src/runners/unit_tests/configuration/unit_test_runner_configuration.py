class UnitTestRunnerConfiguration:
    
    def __init__(self, json_args):
        self.code_file = json_args["code_file"]
        self.language = json_args["language"]        

    