from langchain.agents import  Tool
from langchain.tools import BaseTool, StructuredTool
import importlib
from typing import cast
from ai.agent_tools.utilities.tool_header import ToolHeader

def create_self_ask_tool(tool_json, memory, override_llm) -> Tool:

    header = ToolHeader(tool_json)

    run_locally = tool_json["run_locally"]
    verbose = tool_json["verbose"]
    max_tokens = tool_json["max_tokens"]

    self_ask_tool_arguments = tool_json["arguments"]       

    search_tool = TOOL_TYPES[tool_json["arguments"]["tool_class_name"]](self_ask_tool_arguments, memory, override_llm)
    
    module = importlib.import_module(header.tool_module_name)

    # dynamically instantiate the tool based on the parameters
    tool_instance = getattr(module, header.tool_class_name)(memory, run_locally, search_tool, verbose, max_tokens, override_llm=override_llm)
    typed_instance = cast(BaseTool, tool_instance)

    tool = Tool(
        name=header.tool_name,
        func=typed_instance.run,
        description=header.tool_description
    )

    return tool


def create_vector_store_retrieval_qa_tool(tool_json, memory, override_llm) -> Tool: 

    header = ToolHeader(tool_json)

    vector_store_retrieval_qa_tool_args = get_vector_store_retrieval_qa_tool_args(tool_json["arguments"])

    module = importlib.import_module(header.tool_module_name)

    # dynamically instantiate the tool based on the parameters
    tool_instance = getattr(module, header.tool_class_name)(memory, **vector_store_retrieval_qa_tool_args, override_llm=override_llm)
    typed_instance = cast(BaseTool, tool_instance)
    
    tool = Tool(
        name=header.tool_name,
        func=typed_instance.run,
        description=header.tool_description,
        return_direct = vector_store_retrieval_qa_tool_args["return_direct"]
    )

    return tool

def create_vector_store_search_tool(tool_json, memory, override_llm):
   
    header = ToolHeader(tool_json)
    database_names = tool_json["arguments"]["database_names"]
    run_locally = tool_json["arguments"]["run_locally"]
    return_direct = tool_json["arguments"]["return_direct"]
    return_source_documents = tool_json["arguments"]["return_source_documents"]
    
    module = importlib.import_module(header.tool_module_name)

    # dynamically instantiate the tool based on the parameters
    tool_instance = getattr(module, header.tool_class_name)(database_names=database_names, run_locally=run_locally, return_source_documents=return_source_documents)
    typed_instance = cast(BaseTool, tool_instance)
    
    tool = StructuredTool.from_function(typed_instance.run, header.tool_name, header.tool_description, return_direct)

    return tool

def create_cvss_tool(tool_json, memory, override_llm):
    header = ToolHeader(tool_json)

    return_direct = tool_json["return_direct"]

    module = importlib.import_module(header.tool_module_name)

    # dynamically instantiate the tool based on the parameters
    tool_instance = getattr(module, header.tool_class_name)()
    typed_instance = cast(BaseTool, tool_instance)
    
    tool = StructuredTool.from_function(typed_instance.run, header.tool_name, header.tool_description, return_direct)

    return tool

def get_vector_store_retrieval_qa_tool_args(tool_json):
    return {
        "run_locally": tool_json["run_locally"],
        "database_name" : tool_json["database_name"],
        "top_k" : tool_json["top_k"],
        "search_type" : tool_json["search_type"],
        "search_distance" : tool_json["search_distance"],
        "verbose" : tool_json["verbose"],
        "max_tokens" : tool_json["max_tokens"],
        "return_source_documents" : tool_json["return_source_documents"],
        "return_direct" : tool_json["return_direct"],
        "chain_type": tool_json["chain_type"],
    }

TOOL_TYPES = {
    "SelfAskAgentTool": create_self_ask_tool,
    "VectorStoreRetrievalQATool": create_vector_store_retrieval_qa_tool,
    "VectorStoreSearchTool": create_vector_store_search_tool,
    "CVSSTool": create_cvss_tool,
    } 