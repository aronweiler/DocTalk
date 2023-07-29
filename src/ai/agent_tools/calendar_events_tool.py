from datetime import datetime, timedelta
from dateutil.parser import parse
import json

from utilities.date_time_utilities import generate_time_string
from ai.agent_tools.calendar.calendar_setup import get_calendar_service
from ai.agent_tools.utilities.abstract_tool import AbstractTool



class CalendarEventsTool(AbstractTool):
    def configure(
        self, memory=None, override_llm=None, json_args=None
    ) -> None:
        pass

    def run(self, query: str) -> str:
        # input is a json string
        json_args = json.loads(query)
        calendar_id = json_args["calendar_id"]

        # What the fuck google... making me write this whole goddamn module
        start_date = self.get_date(json_args, "start_date")        
        end_date = self.get_date(json_args, "end_date", start_date)
        
        # If the end_date in the argument is the same as the start date, add 1 to make sure we capture the whole day
        if start_date == end_date:
            end_date = end_date + timedelta(days=1)

        # Get the time string that google expects 
        # ffff... what pain in the ass, I am probably making this way more complex than it needs to be
        start_time = generate_time_string(start_date)
        end_time = generate_time_string(end_date)

        service = get_calendar_service()

        events_result = (
            service.events()
            .list(
                calendarId=calendar_id,
                timeMin=start_time,
                timeMax=end_time,
                maxResults=10,
                singleEvents=True,
                orderBy="startTime",
            )
            .execute()
        )
        events = events_result.get("items", [])

        if not events or len(events) == 0:
            msg = f'No events were found for your {events_result.get("summary", "primary")} calendar for the specified date'
            # Add an 's' to the end of msg if the end_date was not specified in the json
            if "end_date" in json_args:
                msg += " range"
            return msg

        return "\n".join([f"{json.dumps(e['start'])}: {e['summary']}" for e in events])

    def get_date(self, json_args, date_field, default = datetime.now().date()):
        try:
            if date_field in json_args:
                date_string = json_args[date_field]

                date = parse(date_string).date()
            else:
                date = default
        except:
            date = default

        return date
    