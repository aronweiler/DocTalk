class AIResult:

    def __init__(self, result_string, source_documents = None) -> None:
        self.result = result_string        
        self.source_documents = source_documents