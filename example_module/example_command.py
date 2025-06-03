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