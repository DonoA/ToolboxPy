import argparse
from toolbox.lib import ToolboxCommand
import subprocess

class UpdateCommand(ToolboxCommand):

    def description(self):
        return "Update all installed modules."

    def get_args(self, parser: argparse.ArgumentParser):
        pass

    def execute(self, args: argparse.Namespace):
        for module in ToolboxCommand.module_config.modules:
            print(f"Updating module {module.name} at {module.install_location}")
            if module.install_type == ToolboxCommand.module_config.GIT:
                self.update_git_module(module)
            elif module.install_type == ToolboxCommand.module_config.LOCAL:
                print(f"Skipping local module {module.name} as it does not require updates.")
            else:
                print(f"Unknown module type {module.install_type} for {module.name}. Skipping update.")

    def update_git_module(self, module):
        try:
            subprocess.run(["git", "-C", module.install_location, "pull"], check=True)
            print(f"Module {module.name} updated successfully.")
        except subprocess.CalledProcessError as e:
            print(f"Error updating git module {module.name}: {e}")
        except FileNotFoundError:
            print(f"Error: Git command not found. Please ensure Git is installed and in your system's PATH.")
        except Exception as e:
            print(f"An unexpected error occurred while updating {module.name}: {e}")

ToolboxCommand.register_root("update", UpdateCommand())