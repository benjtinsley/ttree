from rich.console import Console
from rich.table import Table
from rich.box import SIMPLE
from rich.panel import Panel
import unittest

class RichTestResult(unittest.TestResult):
    def __init__(self, console, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.console = console
        self.table = Table(box=SIMPLE)
        self.table.add_column("Group", style="magenta")
        self.table.add_column("Test", style="cyan")
        self.table.add_column("Result", style="magenta")
        self.error_details = []

    def add_result(self, test, outcome):
        test_class_name = test.__class__.__name__
        test_method_name = test._testMethodName
        self.table.add_row(test_class_name, test_method_name, outcome)

    def addSuccess(self, test):
        self.add_result(test, "[green]PASS[/green]")

    def addError(self, test, err):
        error_message = self._exc_info_to_string(err, test)
        self.add_result(test, "[red]ERROR[/red]")
        self.error_details.append(f"{test}: {error_message}")

    def addFailure(self, test, err):
        error_message = self._exc_info_to_string(err, test)
        self.add_result(test, "[red]FAIL[/red]")
        self.error_details.append(f"{test}: {error_message}")

    def addSkip(self, test, reason):
        self.add_result(test, f"[yellow]SKIPPED[/yellow] ({reason})")

class RichTestRunner(unittest.TextTestRunner):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.console = Console()

    def run(self, test):
        "Run the given test case or test suite."
        result = RichTestResult(self.console)
        test(result)
        self.console.print(result.table)

        if result.error_details:
            error_panel = Panel("\n".join(result.error_details), title="Detailed Errors", expand=False)
            self.console.print(error_panel)

        return result