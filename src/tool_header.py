class ToolHeader:
    def __init__(self, tool_json):
        self.tool_name = tool_json["friendly_name"]
        self.tool_description = tool_json["description"]
        self.tool_class_name = tool_json["tool_class_name"]
        self.tool_module_name = tool_json["tool_module_name"]