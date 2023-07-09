from fastapi import FastAPI
import uvicorn
from ai.abstract_ai import AbstractAI
from runner.runner import Runner

class RestAPIRunner(Runner):
    def __init__(self):
        super().__init__()
        self.app = FastAPI()

    def query_ai(self, query: str):
        print(f"Querying abstract AI, '{query}'")
        return {"result": self.abstract_ai.query(query)}

    def run(self, abstract_ai: AbstractAI):
        self.abstract_ai = abstract_ai
        uvicorn.run(self.app, host="0.0.0.0", port=8100)

    def __call__(self, abstract_ai: AbstractAI):
        @self.app.get("/query")
        def query_endpoint(query: str):
            return self.query_ai(query)

        self.run(abstract_ai)

# Example usage
# if __name__ == "__main__":
#     ai_instance = AbstractAI()  
#     api = RestAPI()
#     api(ai_instance)  
