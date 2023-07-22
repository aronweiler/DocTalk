import python_weather
import json
import asyncio
import os

from ai.agent_tools.utilities.abstract_tool import AbstractTool

class WeatherTool(AbstractTool):

    async def configure(self, memory = None, override_llm = None, json_args = None) -> None:           
        if os.name == 'nt':
            asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())        
        

    def run(self, query:str) -> str:
        # Call the async get method synchronously
        #loop = asyncio.new_event_loop()

        try:
            result = asyncio.run(self.get(query))
        except asyncio.TimeoutError:
            return "Timeout: The operation took too long to complete."

        # f"In {query} it is {result.current.description}, and the temperature is {result.current.temperature} degrees."
        return f"Feels like: {result.current.feels_like} degrees. Temperature: {result.current.temperature} degrees. Description: {result.current.description}. Humidity: {result.current.humidity}. Wind speed: {result.current.wind_speed}. Wind direction: {result.current.wind_direction}. Visibility: {result.current.visibility}."
    

    async def get(self, query):
        weather_client = python_weather.Client(unit=python_weather.IMPERIAL)

        # Get the current weather of the city
        weather = await weather_client.get(query)

        # Return the weather
        return weather