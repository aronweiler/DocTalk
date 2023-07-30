import json
from typing import Union, List
from json import JSONEncoder
from pydantic import TypeAdapter

# For testing
# Add the root path to the python path so we can import the database
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))

class OpenAIConfiguration:
    
    def __init__(self, json_args):
        args = json_args.get("arguments", {})
        self.model = args.get("model", "gpt-3.5-turbo")
        self.use_memory = args.get("use_memory", False)
        self.prompt = args.get("prompt", None)
        self.chat_model = args.get("chat_model", False)
        self.ai_temp = args.get("ai_temp", 0)
        self.verbose = args.get("verbose", False)
        self.max_tokens = args.get("max_tokens", 4096)
        self.tools = ToolLoader.load_tools_from_json(args.get("tools", []))

class OpenAIConfigurationJSONEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, OpenAIToolProperty):
            return obj.__dict__
        if isinstance(obj, OpenAIToolParametersObject):
            return obj.__dict__
        if isinstance(obj, OpenAITool):
            return obj.__dict__        
        return JSONEncoder.default(self, obj)

class OpenAIToolProperty:
    def __init__(self, param_type, description):
        self.type = param_type
        self.description = description

    def to_dict(self):
        return {
            "type": self.type,
            "description": self.description
        }

class OpenAIToolParametersObject:
    def __init__(self, params_type, properties:OpenAIToolProperty, parameters_required = []):
        self.type = params_type
        self.properties = properties
        self.required = parameters_required

    def to_dict(self):
        return {
            "type": self.type,
            "properties": self.properties.to_dict(),
            "required": self.required
        }

class OpenAITool():
    def __init__(self, name, description, parameters:Union[OpenAIToolParametersObject, None]=None):
        self.name = name
        self.description = description        
        self.parameters = parameters or {}

    def to_dict(self):
        return {
            "name": self.name,
            "description": self.description,
            "parameters": self.parameters.to_dict(),
        }

    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)        

class OpenAIToolWrapper:
    def __init__(self, module, class_name, name, tool_configuration, open_ai_tool:OpenAITool):
        self.tool_module = module
        self.tool_class = class_name
        self.name = name
        self.tool_configuration = tool_configuration
        self.open_ai_tool = open_ai_tool

class ToolLoader:
    # static method to load tools
    @staticmethod
    def load_tools_from_json(json_string_list):
        tool_list = []
        for data in json_string_list:
            tool_list.append(ToolLoader.load_tool_from_json(data))
        return tool_list

    @staticmethod
    def load_tool_from_json(data):
        name = data.get("name", "")
        description = data.get("description", "")
        module = data.get("module", "")
        class_name = data.get("class_name", "")
        tool_configuration = data.get("tool_configuration", {})
        properties = {}
        parameters = None
        parameters_required = []

        if "parameters" in data:
            parameters_type = data["parameters"].get("type", "")
            parameters_required = data["parameters"].get("required", [])
            property_data = data["parameters"].get("properties", {})
            
            for property_name, property_info in property_data.items():
                property_type = property_info.get("type", "")
                property_description = property_info.get("description", "")
                properties[property_name] = OpenAIToolProperty(property_type, property_description)
            
            parameters = OpenAIToolParametersObject(params_type=parameters_type, properties=properties, parameters_required=parameters_required)

        open_ai_tool = OpenAITool(name, description, parameters)

        return OpenAIToolWrapper(module=module, class_name=class_name, name=name, tool_configuration=tool_configuration, open_ai_tool=open_ai_tool)



# Testing
if __name__ == "__main__":
    # Sample JSON strings
    json_string_list = [
        """{
            "name": "get_current_weather",
            "description": "Get the current weather",
            "module": "tools.weather",
            "class_name": "WeatherTool",
            "tool_configuration": {
                "api_key": "1234567890",
                "something_else": "blah blah blah"
            },
            "parameters": {
                "type": "object",
                "properties": {
                    "location": {
                        "type": "string",
                        "description": "The city and state, e.g. San Francisco, CA"
                    },
                    "format": {
                        "type": "string",
                        "enum": ["celsius", "fahrenheit"],
                        "description": "The temperature unit to use. Infer this from the users location."
                    }
                },
                "required": ["location", "format"]
            }
        }""",
        """{
            "name": "get_articles",
            "description": "Use this function to get academic papers from arXiv to answer user questions.",
            "module": "tools.articles",
            "class_name": "ArticleTool",
            "tool_configuration": {
                "url": "http://goolge.com",
                "more": "blah blah blah"
            },
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "User query in JSON. Responses should be summarized and should include the article URL reference"
                    }
                },
                "required": [
                    "query"
                ]
            }
        }""",
        """{
            "name": "read_article_and_summarize",
            "description": "Use this function to read whole papers and provide a summary for users. You should NEVER call this function before get_articles has been called in the conversation.",
            "module": "tools.articles",
            "class_name": "ArticleTool",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "Description of the article in plain text based on the user's query"
                    }
                },
                "required": ["query"]
            }
        }""",
        # Add more JSON strings here
    ]

    tool_loader = ToolLoader()

    # Load tools from JSON strings
    tools = tool_loader.load_tools_from_json(json_string_list)

    # Accessing properties using class attributes
    for tool in tools:
        print(f"Tool Name: {tool.name}")
        print(f"Tool Description: {tool.description}")
        print(f"Tool Module: {tool.tool_module}")
        print(f"Tool Class: {tool.tool_class}")
        print(f"Tool Configuration: {tool.tool_configuration}")
        for param in tool.parameters:
            print(f"Parameter Type: {param.type}")
            print(f"Parameter Description: {param.description}")
        print()
