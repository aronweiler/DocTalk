from tenacity import retry, stop_after_attempt, wait_random_exponential
import requests
import json
from ai.open_ai.open_ai_with_tools_configuration import OpenAIConfigurationJSONEncoder
from ai.open_ai.tools.pretty_print import pretty_print_conversation

class OpenAIChatCompletion:
    def __init__(self, openai_api_key, model):
        self.openai_api_key = openai_api_key
        self.model = model

    @retry(wait=wait_random_exponential(multiplier=1, max=40), stop=stop_after_attempt(3))
    def chat_completion_request(self, messages, functions=None, function_call=None):
        headers = {
            "Content-Type": "application/json",
            "Authorization": "Bearer " + str(self.openai_api_key),
        }
        json_data = {"model": self.model, "messages": messages}
        if functions is not None:
            json_data.update({"functions": functions})
        if function_call is not None:
            json_data.update({"function_call": function_call})
        try:
            response = requests.post(
                "https://api.openai.com/v1/chat/completions",
                headers=headers,
                # I fucking hate this
                json=json.loads(json.dumps(json_data, cls=OpenAIConfigurationJSONEncoder)),
            )
            return response
        except Exception as e:
            pretty_print_conversation("Unable to generate ChatCompletion response", "red")
            pretty_print_conversation(f"Exception: {e}", "red")
            return e