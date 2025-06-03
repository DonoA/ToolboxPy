from abc import ABC, abstractmethod
import argparse
from .module_config import ModuleConfig

class ToolboxCommand(ABC):
    module_config: ModuleConfig = None
    current_module_name = None

    all_commands = {}
    root_commands = {}

    @classmethod
    def register(cls, name: str, command: 'ToolboxCommand'):
        module_commands = cls.all_commands.get(cls.current_module_name, dict())
        module_commands[name] = command
        cls.all_commands[cls.current_module_name] = module_commands

    @classmethod
    def register_root(cls, name: str, command: 'ToolboxCommand'):
        cls.root_commands[name] = command

    @abstractmethod
    def description(self):
        return self.__doc__
    
    @abstractmethod
    def get_args(self, parser: argparse.ArgumentParser):
        pass
    
    @abstractmethod
    def execute(self, args: argparse.Namespace):
        pass