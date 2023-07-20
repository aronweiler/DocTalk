from datetime import datetime
from ai.agent_tools.utilities.abstract_tool import AbstractTool

class TimeTool(AbstractTool):

    def configure(self, memory = None, override_llm = None, json_args = None) -> None:
        pass      
        
    def run(self, query:str) -> str:
        return datetime.now().strftime("%A, %B %d, %Y %I:%M %p")
