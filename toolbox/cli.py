import argparse
import os
import importlib
from toolbox.lib import ToolboxCommand, ModuleConfig
import sys

def load_modules(module_config):
    """
    Load all modules specified in the module configuration.
    """

    # Load each module
    for module in module_config.modules:
        module_path = module.install_location
        if os.path.exists(module_path):
            load_module(module_path)
        else:
            print(f"Module path does not exist: {module_path}")


def load_module(module_path):
    module_name = os.path.basename(module_path)
    
    # Set module name so imported commands can register themselves
    ToolboxCommand.current_module_name = module_name

    if "__init__.py" in os.listdir(module_path):
        spec = importlib.util.spec_from_file_location(module_name, os.path.join(module_path, "__init__.py"))
        my_module = importlib.util.module_from_spec(spec)
        sys.modules[module_name] = my_module
        spec.loader.exec_module(my_module)

    else:
        for file in os.listdir(module_path):
            if file.endswith(".py") and file != "__init__.py":
                file_name = file[:-3]
                spec = importlib.util.spec_from_file_location(file_name, os.path.join(module_path, file))
                my_module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(my_module)

def setup_argparse():
    """
    Setup the argument parser for the CLI.
    """

    parser = argparse.ArgumentParser(
        description="Toolbox CLI"
    )

    module_subparser_map = {}

    subparsers = parser.add_subparsers()
    for (name, command) in ToolboxCommand.root_commands.items():
        subparser = subparsers.add_parser(name, help=command.description())
        command.get_args(subparser)

    for (module_name, commands) in ToolboxCommand.all_commands.items():
        module_parser = subparsers.add_parser(module_name, help=f"Commands for {module_name}")
        module_subparser_map[module_name] = module_parser
        subparsers = module_parser.add_subparsers()
        for (name, command) in commands.items():
            subparser = subparsers.add_parser(name, help=command.description())
            command.get_args(subparser)

    return parser, module_subparser_map

def execute_command(parser, parsed_args, module_subparser_map):
    if len(sys.argv) <= 1:
        parser.print_help()
        sys.exit(1)

    command_name = sys.argv[1]
    # Root commands
    if command_name in ToolboxCommand.root_commands:
        command = ToolboxCommand.root_commands[command_name]
        command.execute(parsed_args)

    # Module commands
    elif command_name in ToolboxCommand.all_commands:
        module_subparser = module_subparser_map[command_name]
        # No subcommand provided
        if len(sys.argv) <= 2:
            print(f"Subcommand name is required for module: {command_name}")
            module_subparser.print_help()
            sys.exit(1)

        module_name = sys.argv[2]
        command = ToolboxCommand.all_commands[module_name].get(command_name)
        # Invalid subcommand provided
        if command is None:
            print(f"Command {command_name} not found in module {module_name}")
            module_subparser.print_help()
            sys.exit(1)

        # Execute the command
        command.execute(parsed_args)

    # Unknown command
    else:
        print(f"Unknown command: {command_name}")
        parser.print_help()
        sys.exit(1)

def main():
    module_config = ModuleConfig.load_module_config()
    # Expose module config to ToolboxCommands
    ToolboxCommand.module_config = module_config
    load_modules(module_config)

    parser, module_subparser_map = setup_argparse()
    parsed_args = parser.parse_args()

    execute_command(parser, parsed_args, module_subparser_map)

    ToolboxCommand.module_config.save()


    