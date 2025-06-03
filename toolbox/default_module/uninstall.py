import argparse
from toolbox.lib import ToolboxCommand, ToolboxModule
import subprocess

class UninstallCommand(ToolboxCommand):

    def description(self):
        return "Uninstall a module from the toolbox."

    def get_args(self, parser: argparse.ArgumentParser):
        parser.add_argument(
            "module_name",
            type=str,
            help="Name of the module to install."
        )

    def execute(self, args: argparse.Namespace):
        print(f"Uninstalling module {args.module_name}")
        module = ToolboxCommand.module_config.find_module(args.module_name)
        if not module:
            print(f"Module {args.module_name} not found.")
            return
        
        if module.install_type == ToolboxCommand.module_config.GIT:
            self.remove_git_module(module)
        elif module.install_type == ToolboxCommand.module_config.LOCAL:
            self.remove_symlink_module(module)
        else:
            print(f"Unknown module type {module.install_type}.")
            return
    
        ToolboxCommand.module_config.modules.remove(module)
        print(f"Module {args.module_name} uninstalled successfully.")

    def remove_git_module(self, module: ToolboxModule):
        try:
            subprocess.run(["rm", "-rf", module.install_location], check=True)
            print(f"Removed git module {module.name} from {module.install_location}")
        except subprocess.CalledProcessError as e:
            print(f"Error removing git module: {e}")
        except FileNotFoundError:
            print(f"Error: Module path not found: {module.install_location}")
        except Exception as e:
            # Catch any other unexpected errors
            print(f"An unexpected error occurred: {e}")
        return None

    def remove_symlink_module(self, module: ToolboxModule):
        try:
            subprocess.run(["rm", module.install_location], check=True)
            print(f"Removed local module {module.name} from {module.install_location}")
        except subprocess.CalledProcessError as e:
            print(f"Error removing symlink module: {e}")
        except FileNotFoundError:
            print(f"Error: Module path not found: {module.install_location}")
        except Exception as e:
            # Catch any other unexpected errors
            print(f"An unexpected error occurred: {e}")
        return None

ToolboxCommand.register_root("uninstall", UninstallCommand())