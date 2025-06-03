import argparse
from toolbox.lib import ToolboxCommand, ModuleConfig, ToolboxModule
import subprocess
import os

class InstallCommand(ToolboxCommand):

    def description(self):
        return "Install a module in the toolbox."

    def get_args(self, parser: argparse.ArgumentParser):
        parser.add_argument(
            "type",
            choices=["git", "local"],
            help="Source to install the module from."
        )
        parser.add_argument(
            "module_source",
            type=str,
            help="Source of the module to install."
        )

    def execute(self, args: argparse.Namespace):
        print(f"Installing module {args.module_source} from {args.type} source.")
        if args.type.lower() == ModuleConfig.GIT:
            print(f"Cloning from {args.module_source}")
            new_module = self.clone_from_git(args.module_source)
        elif args.type.lower() == ModuleConfig.LOCAL:
            print(f"Linking from {args.module_source}")
            new_module = self.symlink_folder(args.module_source)
        else:
            print(f"Unknown module source type {args.type}.")
            return
        
        if new_module:
            print(f"Module {new_module.name} installed successfully.")
            ToolboxCommand.module_config.modules.append(new_module)
        
    def clone_from_git(self, module_source: str):
        module_name = module_source.split("/")[-1].replace(".git", "")
        destination = ModuleConfig.get_module_path(module_name)
        try:
            subprocess.run(["git", "clone", module_source, destination], check=True)

            return ToolboxModule(
                name=module_name,
                install_location=destination,
                install_type=ModuleConfig.GIT,
                install_source=module_source
            )
        except subprocess.CalledProcessError as e:
            print(f"Error cloning git repo: {e}")
        except FileNotFoundError:
            print("Error: Git command not found. Please ensure Git is installed and in your system's PATH.")
        except Exception as e:
            # Catch any other unexpected errors
            print(f"An unexpected error occurred: {e}")
        
        return None
    
    def symlink_folder(self, module_source: str):
        module_name = module_source.split("/")[-1]
        destination = ModuleConfig.get_module_path(module_name)
        full_source_path = os.path.abspath(module_source)
        try:
            subprocess.run(["ln", "-s", full_source_path, destination], check=True)

            return ToolboxModule(
                name=module_name,
                install_location=destination,
                install_type=ModuleConfig.LOCAL,
                install_source=module_source
            )
        except subprocess.CalledProcessError as e:
            print(f"Error creating symlink: {e}")
        except FileNotFoundError:
            print("Error: Source folder not found.")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
        
        return None


ToolboxCommand.register_root("install", InstallCommand())