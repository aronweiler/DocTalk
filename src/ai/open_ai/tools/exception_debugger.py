import openai
import logging

from ai.open_ai.open_ai_chat_completion import OpenAIChatCompletion
from ai.open_ai.tools.pretty_print import pretty_print_conversation

class ExceptionDebugger:
    def __init__(self, api_key, model):
        self.api_key = api_key
        openai.api_key = api_key
        self.model = model

    def debug_exception(self, exception, model = None, print_summary=True):
        if model is None:
            model = self.model
            
        open_ai_chat_completion = OpenAIChatCompletion(self.api_key, self.model)

        # Convert the exception into a string for GPT-3.5-turbo input
        exception_text = f"Please diagnose this exception for me:\n{type(exception).__name__}: {str(exception)}"

        messages = []
        messages.append({"role": "system", "content": "You are a helpful programmer who is debugging a program."})
        messages.append({"role": "user", "content": "Give me your best guess as to why this is happening."})
        messages.append({"role": "user", "content": "Include examples of how I might troubleshoot this."})
        messages.append({"role": "user", "content": exception_text})        

        # Call GPT-3.5-turbo to get the debugging results
        # response = openai.ChatCompletion.create(
        #     engine=model,  # Use GPT-3.5-turbo engine
        #     prompt=exception_text,
        #     max_tokens=200,
        #     stop=None,  # Let GPT-3.5-turbo decide when to stop generating output
        # )

        # Extract the summary from the response
        chat_response = open_ai_chat_completion.chat_completion_request(
            messages
        )            

        if chat_response.status_code != 200:
            pretty_print_conversation(chat_response.json(), "red")
        else:
            assistant_message = chat_response.json()["choices"][0]["message"]
            messages.append(assistant_message)
            pretty_print_conversation(assistant_message, "blue")

            return messages
        
