class ToolboxModule:
    def __init__(self, name, install_location, install_type, install_source):
        self.name = name
        self.install_location = install_location
        self.install_type = install_type
        self.install_source = install_source

    @classmethod
    def from_json(cls, json_data):
        """
        Load the module configuration from a JSON object.
        """
        return ToolboxModule(
            name=json_data.get("name"),
            install_location=json_data.get("install_location"),
            install_type=json_data.get("install_type"),
            install_source=json_data.get("install_source")
        )
    
    def as_dict(self):
        return self.__dict__