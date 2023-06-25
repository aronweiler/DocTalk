from langchain.agents import  Tool
from langchain.tools import BaseTool
import importlib
from typing import cast

def create_self_ask_tool(tool_json, memory) -> Tool:
    """Creates a tool from a JSON representation"""        
    tool_name = tool_json["friendly_name"]
    tool_description = tool_json["description"]
    tool_module_name = tool_json["tool_module_name"]
    tool_class_name = tool_json["tool_class_name"]
    run_locally = tool_json["run_locally"]
    verbose = tool_json["verbose"]
    max_tokens = tool_json["max_tokens"]

    self_ask_tool_arguments = tool_json["arguments"]       

    search_tool = TOOL_TYPES[tool_json["arguments"]["tool_class_name"]](self_ask_tool_arguments, memory)
    
    module = importlib.import_module(tool_module_name)

    # dynamically instantiate the tool based on the parameters
    tool_instance = getattr(module, tool_class_name)(memory, run_locally, search_tool, verbose, max_tokens)
    typed_instance = cast(BaseTool, tool_instance)

    tool = Tool(
        name=tool_name,
        func=typed_instance.run,
        description=tool_description
    )

    return tool

def create_vector_store_tool(tool_json, memory) -> Tool: 
    """Creates a tool from a JSON representation"""        
    tool_name = tool_json["friendly_name"]
    tool_description = tool_json["description"]
    tool_class_name = tool_json["tool_class_name"]
    tool_module_name = tool_json["tool_module_name"]

    vector_store_tool_args = get_vector_store_tool_args(tool_json["arguments"])

    module = importlib.import_module(tool_module_name)

    # dynamically instantiate the tool based on the parameters
    tool_instance = getattr(module, tool_class_name)(memory, **vector_store_tool_args)
    typed_instance = cast(BaseTool, tool_instance)
    
    tool = Tool(
        name=tool_name,
        func=typed_instance.run,
        description=tool_description,
        return_direct = vector_store_tool_args["return_direct"]
    )

    return tool

def get_vector_store_tool_args(tool_json):
    return {
        "run_locally": tool_json["run_locally"],
        "database_name" : tool_json["database_name"],
        "top_k" : tool_json["top_k"],
        "search_type" : tool_json["search_type"],
        "search_distance" : tool_json["search_distance"],
        "verbose" : tool_json["verbose"],
        "max_tokens" : tool_json["max_tokens"],
        "return_source_documents" : tool_json["return_source_documents"],
        "return_direct" : tool_json["return_direct"]
    }

TOOL_TYPES = {
    "SelfAskAgentTool": create_self_ask_tool,
    "VectorStoreTool": create_vector_store_tool
    } 