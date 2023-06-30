import json
import tool_creator
from tool_header import ToolHeader

def load_tools(config, memory, override_llm):
    tools = []

    for tool_json in config["tools"]:
        # Load the JSON into the specified type, getting the tool back
        header = ToolHeader(tool_json)
        tool = tool_creator.TOOL_TYPES[header.tool_class_name](tool_json, memory, override_llm)
        tools.append(tool)
    
    return tools

def load_tools_from_file(tool_config_path, memory, override_llm):
    
    with open(tool_config_path) as config_file:
        config = json.load(config_file)

    return load_tools(config, memory, override_llm)