import datetime
import json
from ai.agent_tools.calendar.calendar_setup import get_calendar_service
from ai.agent_tools.utilities.abstract_tool import AbstractTool


class ListCalendarsTool(AbstractTool):
    def configure(
        self, registered_settings, memory=None, override_llm=None, json_args=None
    ) -> None:
        pass

    def run(self, query: str) -> str:
        service = get_calendar_service()

        calendars_result = service.calendarList().list().execute()

        calendars = calendars_result.get("items", [])

        if not calendars:
            return "No calendars found."

        calendars_descriptions = [{}]
        for calendar in calendars:
            calendars_descriptions.append({
                "summary": calendar["summary"],
                "calendar_id": calendar["id"],
                "is_primary": "True" if calendar.get("primary") else "False"
            })            

        return json.dumps(calendars_descriptions)