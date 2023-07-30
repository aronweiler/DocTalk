import logging
import json
from tenacity import retry, wait_random_exponential, stop_after_attempt
import openai
import requests


# For testing
# Add the root path to the python path so we can import the database
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))

from utilities.token_helper import num_tokens_from_string
from ai.open_ai.open_ai_with_tools_configuration import OpenAIConfiguration
from ai.abstract_ai import AbstractAI
from ai.ai_result import AIResult

from ai.open_ai.tool_creator import create_tool
from ai.open_ai.open_ai_with_tools_configuration import OpenAIConfigurationJSONEncoder
from ai.open_ai.tools.exception_debugger import ExceptionDebugger
from ai.open_ai.open_ai_chat_completion import OpenAIChatCompletion
from ai.open_ai.tools.pretty_print import pretty_print_conversation


class OpenAIWithTools(AbstractAI):
    def configure(self, json_args) -> None:
        self.configuration = OpenAIConfiguration(json_args)
        self.openai_api_key = self.get_openai_api_key()

        self.tools = self.create_openai_tools()

        self.open_ai_completion = OpenAIChatCompletion(
            self.openai_api_key, self.configuration.model
        )

        if logging.getLogger().isEnabledFor(logging.DEBUG):
            self.exception_debugger = ExceptionDebugger(
                self.openai_api_key, self.configuration.model
            )

    def get_openai_api_key(self):
        from dotenv import dotenv_values, load_dotenv

        load_dotenv()
        return dotenv_values().get("OPENAI_API_KEY")

    # Creates a dictionary of tools that can be used by the AI
    def create_openai_tools(self):
        tools = {}
        for tool in self.configuration.tools:
            # Create a tool_instance from the configuration
            tool_instance = create_tool(tool)

            tools[tool.open_ai_tool.name] = tool_instance
        return tools

    def query(self, input):
        pass

    def break_into_steps(self, input, messages=[]):
        messages.append({"role": "assistant", "content": "I will take the following request and break it into the most granular pieces I can in order to develop a plan to answer this query:"})
        messages.append({"role": "user", "content": input})
        messages.append({"role": "assistant", "content": "Here is a list of the step names I would need to take to answer your query:"})

        return self.process(messages)

    def execute_step(self, messages=[]):
        messages.append({"role": "user", "content": "Please complete the next step in the list, if you are done, please type 'done'"})
        #messages.append({"role": "assistant", "content": "Here is a list of the step names I would need to take to answer your query:"})
        return self.process(messages)
            
    def process(self, messages):
        try:
            chat_response = self.open_ai_completion.chat_completion_request(
                messages,
                functions=[t.open_ai_tool for t in self.configuration.tools],
            )
            
            if chat_response.status_code != 200:
                raise Exception(
                    f"OpenAI returned a non-200 status code: {chat_response.status_code}.  Response: {chat_response.text}"
                )

            assistant_message = chat_response.json()["choices"][0]["message"]
            messages.append(assistant_message)

            pretty_print_conversation(messages)

            return messages

        except Exception as e:
            if self.exception_debugger:
                _ = self.exception_debugger.debug_exception(e, print_summary=True)

    #     num_tokens = 0

    #     ai_results = AIResult(result, result["text"])

    #     return ai_results


# Testing - doesn't work anymore
if __name__ == "__main__":
    # set logging to DEBUG
    logging.basicConfig(level=logging.DEBUG)

    openai_with_tools = OpenAIWithTools()
    with open("src\\ai\\open_ai\\sample.json") as config_file:
        config_json = json.load(config_file)

    openai_with_tools.configure(config_json["ai"])

    openai_with_tools.create_openai_tools()

    messages = []
    messages.append(
        {
            "role": "system",
            "content": "It is July 28th, 2023.  The user is located in San Diego, CA.  Their email address is aronweiler@gmail.com",
        }
    )

    result = messages

    while True:
        user_input = input("Enter a message:")
        # First break the request down into pieces if possible
        result = openai_with_tools.break_into_steps(user_input, result)

        # If the last step is a function call, ask the user for the answer
        if "function_call" in result[len(result) - 1]:
            result.append({"role": "user", "content": input("Fake function call answer:")})

        while True:
            result = openai_with_tools.execute_step(result)

            if "function_call" in result[len(result) - 1]:
                result.append({"role": "user", "content": input("Fake function call answer:")})
            elif result[len(result) - 1]["content"] == "done":
                break
            else:
                result.append({"role": "user", "content": input("Enter message:")})
                openai_with_tools.process(result)
                break
                
            

