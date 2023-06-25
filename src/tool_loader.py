import json
import tool_creator

def load_tools(config, memory):
    tools = []

    for tool_json in config["tools"]:
        # Load the JSON into the specified type, getting the tool back
        tool = tool_creator.TOOL_TYPES[tool_json["tool_class_name"]](tool_json, memory)
        tools.append(tool)
    
    return tools

def load_tools_from_file(tool_config_path, memory):
    
    with open(tool_config_path) as config_file:
        config = json.load(config_file)

    return load_tools(config, memory)