import logging
import importlib

from ai.open_ai.open_ai_with_tools_configuration import OpenAIToolWrapper


def create_tool(open_ai_tool:OpenAIToolWrapper):
    if open_ai_tool is None:
        raise Exception("open_ai_tool must be provided")

    try:
        module = importlib.import_module(open_ai_tool.tool_module)

        # dynamically instantiate the tool based on the parameters
        tool_instance = getattr(module, open_ai_tool.tool_class)(open_ai_tool.tool_configuration)        

        return tool_instance
    except Exception as e:
        logging.error("Error creating tool: " + str(e))

    return None
