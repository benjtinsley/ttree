import unittest
from rich.console import Console
from rich.table import Table
from rich.box import SIMPLE
from rich.panel import Panel
from rich.text import Text
import re

class RichTestResult(unittest.TestResult):
    def __init__(self, console, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.console = console
        self.table = Table(box=SIMPLE)
        self.table.add_column("Class", style="cyan")
        self.table.add_column("Test", style="cyan")
        self.table.add_column("Result", style="magenta")
        self.error_details = []

    def add_result(self, test, outcome):
        test_class_name = test.__class__.__name__
        test_method_name = test._testMethodName
        self.table.add_row(test_class_name, test_method_name, outcome)

    def addSuccess(self, test):
        super().addSuccess(test)
        self.add_result(test, "[green]PASS[/green]")
    
    def addError(self, test, err):
        error_message = self._exc_info_to_string(err, test)
        self.add_result(test, "[red]ERROR[/red]")
        self.error_details.append((test, error_message))

    def addFailure(self, test, err):
        error_message = self._exc_info_to_string(err, test)
        self.add_result(test, "[red]FAIL[/red]")
        self.error_details.append((test, error_message))

    def addSkip(self, test, reason):
        self.add_result(test, f"[yellow]SKIPPED[/yellow] ({reason})")

    def _exc_info_to_string(self, err, test):
        """Converts exception info into a string with rich formatting."""
        error_message = super()._exc_info_to_string(err, test)

        rich_text = Text()

        # Split the message by lines to apply styles to specific parts
        for line in error_message.splitlines():
            if 'AssertionError' in line:
                rich_text.append(line + '\n', style="bold red")
            elif 'File "' in line and '", line' in line:
                # Apply underline style to file paths
                parts = line.split('"')
                rich_text.append(parts[0] + '"')
                rich_text.append(parts[1], style="underline")
                rich_text.append('"' + parts[2] + '\n')
            else:
                rich_text.append(line + '\n')

        return rich_text


class RichTestRunner(unittest.TextTestRunner):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.console = Console()

    def run(self, test):
        result = RichTestResult(self.console)
        test(result)
        self.console.print(result.table)

        if result.error_details:
            for test, error_message in result.error_details:
                test_name = f"{test.__class__.__name__}.{test._testMethodName}"
                error_panel = Panel(error_message, title=f"Error Details for: [bold magenta]{test_name}[/]", expand=False)
                self.console.print(error_panel)

        return result