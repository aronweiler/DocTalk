import json
from langchain.agents import  Tool
from langchain.tools import BaseTool
import importlib
from typing import cast, Callable


def create_tool(tool_json) -> Tool: 
    """Creates a tool from a JSON representation"""        
    tool_name = tool_json["friendly_name"]
    tool_description = tool_json["description"]
    tool_class_name = tool_json["tool_class_name"]
    tool_module_name = tool_json["tool_module_name"]

    run_locally = tool_json["arguments"]["run_locally"]
    database_name = tool_json["arguments"]["database_name"]
    top_k = tool_json["arguments"]["top_k"]
    search_type = tool_json["arguments"]["search_type"]
    search_distance = tool_json["arguments"]["search_distance"]
    verbose = tool_json["arguments"]["verbose"]
    max_tokens = tool_json["arguments"]["max_tokens"]
    return_source_documents = tool_json["arguments"]["return_source_documents"]
    return_direct = tool_json["arguments"]["return_direct"]

    module = importlib.import_module(tool_module_name)

    # dynamically instantiate the tool based on the parameters
    tool_instance = getattr(module, tool_class_name)(database_name, run_locally, top_k, search_type, search_distance, verbose, max_tokens, return_source_documents)
    typed_instance = cast(BaseTool, tool_instance)
    
    tool = Tool(
        name=tool_name,
        func=typed_instance.run,
        description=tool_description,
        return_direct = return_direct
    )

    return tool

def load_tools(tool_config_path):
    
    with open(tool_config_path) as config_file:
        config = json.load(config_file)

    tools = []

    for tool_json in config["tools"]:
        tool = create_tool(tool_json)
        tools.append(tool)

    return tools

# tools = load_tools('C:\\Repos\\DocTalk\\tool_configurations\\medical_device_config.json')
# result = tools[0].run("What does the FDA say about SBOMs?")
# print(result)