import datetime
import json
from ai.agent_tools.calendar.calendar_setup import get_calendar_service
from ai.agent_tools.utilities.abstract_tool import AbstractTool

class CalendarEventsTool(AbstractTool):

    def configure(self, registered_settings, memory = None, override_llm = None, json_args = None) -> None:
        pass      
        
    def run(self, query:str) -> str:
        service = get_calendar_service()
        
        now = datetime.datetime.utcnow().isoformat() + 'Z'
        
        events_result = service.events().list(calendarId=query, timeMin=now, maxResults=10, singleEvents=True, orderBy='startTime').execute()
        events = events_result.get('items', [])

        return "\n".join([f"{json.dumps(e['start'])}: {e['summary']}" for e in events])