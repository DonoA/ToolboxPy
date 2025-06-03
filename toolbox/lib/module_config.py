from .toolbox_module import ToolboxModule
from toolbox import ROOT_DIR
import os, json
from pathlib import Path
from typing import List

class ModuleConfig:
    GIT = "git"
    LOCAL = "local"
    SYSTEM = "system"

    def __init__(self, config_version=None, modules=None):
        self.config_version = config_version or "1.0"
        self.modules: List[ToolboxModule] = modules or []

    @classmethod
    def from_json(clss, json_data):
        """
        Load the module configuration from a JSON object.
        """
        return ModuleConfig(
            config_version=json_data.get("config_version"),
            modules=[
                ToolboxModule.from_json(data) 
                for data in json_data.get("modules", [])
            ]
        )
    
    def save(self):
        """
        Save the module configuration to a JSON file.
        """
        config_path = os.path.join(ModuleConfig.toolbox_folder(), "config.json")
        os.makedirs(os.path.dirname(config_path), exist_ok=True)
        
        with open(config_path, "w") as f:
            json.dump(self.as_dict(), f, indent=4)

    def as_dict(self):
        return {
            "config_version": self.config_version,
            "modules": [module.as_dict() for module in self.modules]
        }
    
    def find_module(self, module_name) -> ToolboxModule:
        """
        Get a module by its name.
        """
        for module in self.modules:
            if module.name == module_name:
                return module
        return None
    
    @classmethod
    def toolbox_folder(clss):
        home = str(Path.home())
        return os.path.join(home, ".toolbox")
    
    @classmethod
    def get_default_config(clss):
        return ModuleConfig(
            modules=[
                ToolboxModule(
                    name="default_module",
                    install_location=os.path.join(ROOT_DIR, "default_module"),
                    install_type="local",
                    install_source=ModuleConfig.SYSTEM
                )
            ]
        )
    
    @classmethod
    def load_module_config(clss):
        """
        Load the module configuration from the config file.
        """

        # Get the path to the user's home directory
        config_path = os.path.join(ModuleConfig.toolbox_folder(), "config.json")

        # Check if the config file exists
        if not os.path.exists(config_path):
            print(f"Config file does not exist: {config_path}")
            return ModuleConfig.get_default_config()

        try:
            # Load the config file
            with open(config_path, "r") as f:
                config_data = json.load(f)
                config = ModuleConfig.from_json(config_data)
            
            return config
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON: {e}")
            return ModuleConfig.get_default_config()
        
    @classmethod
    def get_module_path(clss, module_name):
        """
        Get the path to the module.
        """
        return os.path.join(ModuleConfig.toolbox_folder(), "modules", module_name)
        
    
    