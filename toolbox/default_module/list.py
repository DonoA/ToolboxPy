import argparse
from toolbox.lib import ToolboxCommand

class ListCommand(ToolboxCommand):

    def description(self):
        return "List all modules and available commands in the toolbox."

    def get_args(self, parser: argparse.ArgumentParser):
        pass

    def execute(self, args: argparse.Namespace):
        print(f"Modules:")
        for module in ToolboxCommand.module_config.modules:
            print(f"  - {module.name} ({module.install_type}, {module.install_location})")

        print(f"Commands:")
        for (name, command) in ToolboxCommand.root_commands.items():
            print(f"  - {name}: {command.description()}")

        for (module_name, commands) in ToolboxCommand.all_commands.items():
            print(f"  - {module_name}:")
            for (name, command) in commands.items():
                print(f"    - {name}: {command.description()}")


ToolboxCommand.register_root("list", ListCommand())