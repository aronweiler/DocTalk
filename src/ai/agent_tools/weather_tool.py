import python_weather
import json
import asyncio
import os
from datetime import datetime
import logging

# For testing
# Add the root path to the python path so we can import the database
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))

from ai.agent_tools.utilities.abstract_tool import AbstractTool


class WeatherTool(AbstractTool):

    def configure(
        self, memory=None, override_llm=None, json_args=None
    ) -> None:
        pass

    def run(self, query: str) -> str:
        # Convert the query to a dictionary
        logging.debug(f"Weather Query: {query}")
        try:
            try:
                json_query = json.loads(query)
                location = json_query["location"]            
            except:
                return "Could not parse the query, make sure your input is valid JSON in the format: {\"location\": \"city, state\", \"date\": \"YYYY-MM-DD\"}"

            # Parse the date string from the query
            date_format = "%Y-%m-%d"
            try:
                if 'date' in json_query:
                    date_string = json_query["date"]
                    parsed_date = datetime.strptime(date_string, date_format).date() 
                else:
                    parsed_date = datetime.now().date()
            except:
                parsed_date = None

            try:   
                
                result = self.get_or_create_eventloop().run_until_complete(self.get(location))         
                #result = asyncio.run(self.get(location))
            except asyncio.TimeoutError:
                return "Timeout: The operation took too long to complete."

            if parsed_date is None or parsed_date == datetime.now().date():
                logging.debug("Looking for the current weather")
                return f"Temperature: {result.current.temperature} degrees. Feels like: {result.current.feels_like} degrees. Description: {result.current.description}. Humidity: {result.current.humidity}."
            else:
                logging.debug("Looking for a forecast for the date: " + str(parsed_date))
                # Look for the date in the forecast
                for forecast in result.forecasts:
                    logging.debug("Forecast date: " + str(forecast.date))
                    if forecast.date == parsed_date:
                        return f"Summarize in one sentence the following hourly forecast for {forecast.date}:\n" + "\n".join([f"Time: {fc.time}, temp: {fc.temperature}, description: {fc.description}" for fc in forecast.hourly])
                        #return f"Low temp: {forecast.lowest_temperature} degrees. High temp: {forecast.highest_temperature} degrees."
                
                return f"Could not find a forecast for {parsed_date}."
        except Exception as e:
            logging.error(e)
            return "An error occurred while processing your request."

    async def get(self, query):
        weather_client = python_weather.Client(unit=python_weather.IMPERIAL)

        # Get the current weather of the city
        weather = await weather_client.get(query)

        # Return the weather
        return weather

    def get_or_create_eventloop(self) -> asyncio.AbstractEventLoop:
        try:
            return asyncio.get_event_loop()
        except RuntimeError as ex:
            if "There is no current event loop in thread" in str(ex):
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                return asyncio.get_event_loop()
            else:
                raise ex
            


# Test code
if __name__ == "__main__":
    tool = WeatherTool()

    result = tool.run("{\"location\": \"San Diego\", \"date\": \"2023-07-29\"}")

    print(result)