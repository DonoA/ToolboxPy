Toolbox
===

Toolbox is an extensible commandline script manager and runner. It provides utilities for easily installing, updating, and managing new script packages. Toolbox can be used to install both local folders and git repos. It provides a simple unified interface for managing commands within small teams or organizations.

## Example Module
Defining a new command is easy:

```python
from toolbox.lib import ToolboxCommand

class ExampleCommand(ToolboxCommand):
    def description(self):
        return "An example command for demonstration purposes."

    def get_args(self, parser):
        parser.add_argument(
            "--example-arg",
            type=str,
            help="An example argument for the command."
        )

    def execute(self, args):
        print(f"Executing ExampleCommand with argument: {args.example_arg}")

ToolboxCommand.register("example", ExampleCommand())
```

to install this new command, install local:
```bash
toolbox install local example_command
```

this will make it visible in the installed packages list
```bash
% toolbox list

Modules:
  - default_module (local, /Users/dallen/projects/toolbox/toolbox/default_module)
  - example_module (local, /Users/dallen/.toolbox/modules/example_module)
Commands:
  - list: List all modules and available commands in the toolbox.
  - install: Install a module in the toolbox.
  - uninstall: Uninstall a module from the toolbox.
  - update: Update all installed modules.
  - example_module:
    - example: An example command for demonstration purposes.
```