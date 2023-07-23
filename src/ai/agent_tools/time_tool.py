import pytz
from datetime import datetime
from ai.agent_tools.utilities.abstract_tool import AbstractTool


class TimeTool(AbstractTool):
    def configure(
        self, registered_settings, memory=None, override_llm=None, json_args=None
    ) -> None:
        pass

    def run(self, query: str) -> str:
        try:
            time_zone = pytz.timezone(query)

            # Get the current datetime in the specified time zone
            current_datetime = datetime.now(time_zone)

            return current_datetime.strftime("%A, %B %d, %Y %I:%M %p")
        except:
            return "Invalid time zone specified."
