TITLE: Initializing Rich Console Object (Python)
DESCRIPTION: This snippet demonstrates how to import the `Console` class from the `rich.console` module and instantiate a `Console` object. This object is the primary interface for controlling rich terminal content.
SOURCE: https://github.com/textualize/rich/blob/master/README.md#_snippet_4

LANGUAGE: python
CODE:
```
from rich.console import Console

console = Console()
```

----------------------------------------

TITLE: Installing Rich Python Library
DESCRIPTION: This command installs the Rich library using pip, the standard Python package installer. It's the recommended way to get Rich set up in your Python environment.
SOURCE: https://github.com/textualize/rich/blob/master/README.md#_snippet_0

LANGUAGE: shell
CODE:
```
python -m pip install rich
```

----------------------------------------

TITLE: Printing Content with Rich Console (Python)
DESCRIPTION: These examples illustrate various uses of the `console.print` method. It can print lists, apply console markup for styling, pretty-print dictionaries (like `locals()`), and apply direct styles using the `style` argument. It converts objects to strings and supports rich content rendering.
SOURCE: https://github.com/textualize/rich/blob/master/docs/source/console.rst#_snippet_2

LANGUAGE: python
CODE:
```
console.print([1, 2, 3])
console.print("[blue underline]Looks like a link")
console.print(locals())
console.print("FOO", style="white on blue")
```

----------------------------------------

TITLE: Installing Rich as Default Traceback Handler
DESCRIPTION: This code installs Rich as the global default traceback handler, ensuring that all subsequent uncaught exceptions are automatically rendered with Rich's enhanced formatting and syntax highlighting. The `show_locals=True` option enables the display of local variables.
SOURCE: https://github.com/textualize/rich/blob/master/docs/source/traceback.rst#_snippet_2

LANGUAGE: Python
CODE:
```
from rich.traceback import install
install(show_locals=True)
```

----------------------------------------

TITLE: Importing Rich's Print Function
DESCRIPTION: This Python statement imports the `print` function from the `rich` library. Once imported, it can be used as a direct drop-in replacement for Python's built-in `print` to automatically apply Rich's enhanced formatting and styling.
SOURCE: https://github.com/textualize/rich/blob/master/docs/source/introduction.rst#_snippet_2

LANGUAGE: Python
CODE:
```
from rich import print
```

----------------------------------------

TITLE: Inspecting Python Objects with Rich Inspect (Python)
DESCRIPTION: This snippet demonstrates how to use the `rich.inspect` function to generate a detailed report on any Python object, such as a class, instance, or builtin. It shows inspecting a list and including its methods in the report.
SOURCE: https://github.com/textualize/rich/blob/master/README.md#_snippet_8

LANGUAGE: python
CODE:
```
my_list = ["foo", "bar"]
from rich import inspect
inspect(my_list, methods=True)
```

----------------------------------------

TITLE: Logging with Rich Console in Python
DESCRIPTION: The `console.log()` method provides enhanced logging capabilities, similar to `print()`, but includes timestamps, file/line information, syntax highlighting for Python structures, and pretty printing for collections. The `log_locals` argument can be used to output a table of local variables for debugging purposes.
SOURCE: https://github.com/textualize/rich/blob/master/README.md#_snippet_9

LANGUAGE: python
CODE:
```
from rich.console import Console
console = Console()

test_data = [
    {"jsonrpc": "2.0", "method": "sum", "params": [None, 1, 2, 4, False, True], "id": "1"},
    {"jsonrpc": "2.0", "method": "notify_hello", "params": [7]},
    {"jsonrpc": "2.0", "method": "subtract", "params": [42, 23], "id": "2"}
]

def test_log():
    enabled = False
    context = {
        "foo": "bar"
    }
    movies = ["Deadpool", "Rise of the Skywalker"]
    console.log("Hello from", console, "!")
    console.log(test_data, log_locals=True)


test_log()
```

----------------------------------------

TITLE: Directly Importing Rich print_json (Python)
DESCRIPTION: This snippet shows how to directly import the `print_json` function from the top-level `rich` module. This provides a convenient shortcut for pretty-printing JSON without needing to instantiate a `Console` object first.
SOURCE: https://github.com/textualize/rich/blob/master/docs/source/console.rst#_snippet_6

LANGUAGE: python
CODE:
```
from rich import print_json
```

----------------------------------------

TITLE: Creating and Printing a Basic Table with Rich in Python
DESCRIPTION: This snippet demonstrates the fundamental steps to create and display a table using the Rich library. It initializes a Table object, defines columns with specific styling and justification, adds rows of data, and then prints the formatted table to the console using a Console instance.
SOURCE: https://github.com/textualize/rich/blob/master/docs/source/tables.rst#_snippet_0

LANGUAGE: Python
CODE:
```
from rich.console import Console
from rich.table import Table

table = Table(title="Star Wars Movies")

table.add_column("Released", justify="right", style="cyan", no_wrap=True)
table.add_column("Title", style="magenta")
table.add_column("Box Office", justify="right", style="green")

table.add_row("Dec 20, 2019", "Star Wars: The Rise of Skywalker", "$952,110,690")
table.add_row("May 25, 2018", "Solo: A Star Wars Story", "$393,151,347")
table.add_row("Dec 15, 2017", "Star Wars Ep. V111: The Last Jedi", "$1,332,539,889")
table.add_row("Dec 16, 2016", "Rogue One: A Star Wars Story", "$1,332,439,889")

console = Console()
console.print(table)
```

----------------------------------------

TITLE: Installing Rich Python Library
DESCRIPTION: This command installs the Rich library from PyPI using pip. It is the standard and recommended way to add Rich to your Python environment, allowing access to its features for rich terminal output.
SOURCE: https://github.com/textualize/rich/blob/master/docs/source/introduction.rst#_snippet_0

LANGUAGE: Bash
CODE:
```
pip install rich
```

----------------------------------------

TITLE: Initializing Rich Console Instance (Python)
DESCRIPTION: This snippet demonstrates how to create a `Console` instance from the `rich.console` module. It's typically created once at the module level to manage terminal output throughout an application.
SOURCE: https://github.com/textualize/rich/blob/master/docs/source/console.rst#_snippet_0

LANGUAGE: python
CODE:
```
from rich.console import Console
console = Console()
```

----------------------------------------

TITLE: Applying Basic Bold and Red Style in Rich
DESCRIPTION: This Python snippet demonstrates the fundamental usage of Rich console markup to apply 'bold' and 'red' styles to a specific part of a string. The `print` function from `rich` is used to render the styled text, with the style applying between the opening `[bold red]` and closing `[/bold red]` tags.
SOURCE: https://github.com/textualize/rich/blob/master/docs/source/markup.rst#_snippet_1

LANGUAGE: Python
CODE:
```
from rich import print
print("[bold red]alert![/bold red] Something happened")
```

----------------------------------------

TITLE: Using Rich Print for Styled Output in Python
DESCRIPTION: This Python snippet demonstrates how to use Rich's `print` function, which replaces the built-in `print` to add color and style to terminal output using Rich's markup. It shows basic text styling and emoji support.
SOURCE: https://github.com/textualize/rich/blob/master/README.md#_snippet_2

LANGUAGE: python
CODE:
```
from rich import print

print("Hello, [bold magenta]World[/bold magenta]!", ":vampire:", locals())
```

----------------------------------------

TITLE: Tracking Task Progress with Rich (Python)
DESCRIPTION: This snippet demonstrates the basic usage of Rich's `track` function to create a simple progress bar for iterating over a sequence. The `track` function wraps an iterable, automatically displaying a flicker-free progress bar in the terminal, which is useful for long-running tasks.
SOURCE: https://github.com/textualize/rich/blob/master/README.md#_snippet_12

LANGUAGE: python
CODE:
```
from rich.progress import track

for step in track(range(100)):
    do_step(step)
```

----------------------------------------

TITLE: Basic Live Display with Rich Table (Python)
DESCRIPTION: Demonstrates how to use `rich.live.Live` as a context manager to display and dynamically update a `rich.table.Table`. It shows adding rows to the table within a loop, with a delay, and the live display refreshing automatically.
SOURCE: https://github.com/textualize/rich/blob/master/docs/source/live.rst#_snippet_0

LANGUAGE: Python
CODE:
```
import time

from rich.live import Live
from rich.table import Table

table = Table()
table.add_column("Row ID")
table.add_column("Description")
table.add_column("Level")

with Live(table, refresh_per_second=4):  # update 4 times a second to feel fluid
    for row in range(12):
        time.sleep(0.4)  # arbitrary delay
        # update the renderable internally
        table.add_row(f"{row}", f"description {row}", "[red]ERROR")
```

----------------------------------------

TITLE: Printing Current Exception Traceback with Rich Console
DESCRIPTION: This snippet demonstrates how to use `console.print_exception()` within an exception handler to display a Rich-formatted traceback for the currently caught exception. The `show_locals=True` parameter includes local variable values for each frame, aiding in debugging.
SOURCE: https://github.com/textualize/rich/blob/master/docs/source/traceback.rst#_snippet_1

LANGUAGE: Python
CODE:
```
from rich.console import Console
console = Console()

try:
    do_something()
except Exception:
    console.print_exception(show_locals=True)
```

----------------------------------------

TITLE: Creating and Styling Tables with Rich (Python)
DESCRIPTION: This example illustrates how to construct and format flexible tables using Rich's `Table` class. It shows how to define columns with styles and justification, add rows of data, and print the table to the console. Rich tables automatically resize columns and wrap text to fit the terminal width.
SOURCE: https://github.com/textualize/rich/blob/master/README.md#_snippet_11

LANGUAGE: python
CODE:
```
from rich.console import Console
from rich.table import Table

console = Console()

table = Table(show_header=True, header_style="bold magenta")
table.add_column("Date", style="dim", width=12)
table.add_column("Title")
table.add_column("Production Budget", justify="right")
table.add_column("Box Office", justify="right")
table.add_row(
    "Dec 20, 2019", "Star Wars: The Rise of Skywalker", "$275,000,000", "$375,126,118"
)
table.add_row(
    "May 25, 2018",
    "[red]Solo[/red]: A Star Wars Story",
    "$275,000,000",
    "$393,151,347"
)
table.add_row(
    "Dec 15, 2017",
    "Star Wars Ep. VIII: The Last Jedi",
    "$262,000,000",
    "[bold]$1,332,539,889[/bold]"
)

console.print(table)
```

----------------------------------------

TITLE: Listing Directory Contents with Rich Columns in Python
DESCRIPTION: This Python script demonstrates how to use the `rich.columns.Columns` class to display directory contents in a columnar format, mimicking the `ls` command. It takes a directory path as a command-line argument, lists its contents using `os.listdir`, and then renders them using `Columns` with `equal=True` and `expand=True` for even distribution across the console.
SOURCE: https://github.com/textualize/rich/blob/master/docs/source/columns.rst#_snippet_0

LANGUAGE: Python
CODE:
```
import os
import sys

from rich import print
from rich.columns import Columns

if len(sys.argv) < 2:
    print("Usage: python columns.py DIRECTORY")
else:
    directory = os.listdir(sys.argv[1])
    columns = Columns(directory, equal=True, expand=True)
    print(columns)
```

----------------------------------------

TITLE: Installing Rich Pretty Printing in Python REPL
DESCRIPTION: This Python code snippet integrates Rich's pretty printing functionality into the Python REPL. Once `pretty.install()` is called, any data structures displayed in the REPL will be automatically formatted and syntax-highlighted by Rich.
SOURCE: https://github.com/textualize/rich/blob/master/README.md#_snippet_3

LANGUAGE: python
CODE:
```
from rich import pretty
pretty.install()
```

----------------------------------------

TITLE: Logging Messages with Rich Console (Python)
DESCRIPTION: This snippet demonstrates the `console.log` method, which is similar to `print` but adds debugging features like timestamps and source file/line information. It's useful for tracking application flow and state.
SOURCE: https://github.com/textualize/rich/blob/master/docs/source/console.rst#_snippet_3

LANGUAGE: python
CODE:
```
console.log("Hello, World!")
```

----------------------------------------

TITLE: Automatic Rich Repr Generation with @rich.repr.auto Decorator in Python
DESCRIPTION: This snippet shows how to automatically generate a Rich representation for a class using the `@rich.repr.auto` decorator. When applied, Rich infers the repr from the class's `__init__` parameters, simplifying the process of creating custom representations without explicit `__rich_repr__` implementation, and also generates a standard `__repr__`.
SOURCE: https://github.com/textualize/rich/blob/master/docs/source/pretty.rst#_snippet_14

LANGUAGE: Python
CODE:
```
import rich.repr

@rich.repr.auto
class Bird:
    def __init__(self, name, eats=None, fly=True, extinct=False):
        self.name = name
        self.eats = list(eats) if eats else []
        self.fly = fly
        self.extinct = extinct


BIRDS = {
    "gull": Bird("gull", eats=["fish", "chips", "ice cream", "sausage rolls"]),
    "penguin": Bird("penguin", eats=["fish"], fly=False),
    "dodo": Bird("dodo", eats=["fruit"], fly=False, extinct=True)
}
from rich import print
print(BIRDS)
```

----------------------------------------

TITLE: Rendering Markdown Content with Rich in Python
DESCRIPTION: This Python snippet shows how to render a Markdown file (README.md) to the terminal using rich.markdown.Markdown. It reads the content of the Markdown file, constructs a Markdown object, and then prints it to the console, translating Markdown formatting into terminal-friendly output.
SOURCE: https://github.com/textualize/rich/blob/master/README.md#_snippet_17

LANGUAGE: python
CODE:
```
from rich.console import Console
from rich.markdown import Markdown

console = Console()
with open("README.md") as readme:
    markdown = Markdown(readme.read())
console.print(markdown)
```

----------------------------------------

TITLE: Creating a Basic Rich Panel
DESCRIPTION: This snippet demonstrates how to create a basic panel using `rich.panel.Panel` to draw a border around text. It imports `print` and `Panel` from the `rich` library and then prints a panel containing the string 'Hello, [red]World!'.
SOURCE: https://github.com/textualize/rich/blob/master/docs/source/panel.rst#_snippet_0

LANGUAGE: Python
CODE:
```
from rich import print
from rich.panel import Panel
print(Panel("Hello, [red]World!"))
```

----------------------------------------

TITLE: Wrapping File-like Objects for Progress Display in Python
DESCRIPTION: This snippet demonstrates using `rich.progress.wrap_file` to add a progress bar to an already open file-like object, such as a network response. It requires specifying the total size of the content to be read. The example simulates reading data from a URL with a delay, showing progress as bytes are consumed.
SOURCE: https://github.com/textualize/rich/blob/master/docs/source/progress.rst#_snippet_11

LANGUAGE: Python
CODE:
```
from time import sleep
    from urllib.request import urlopen

    from rich.progress import wrap_file

    response = urlopen("https://www.textualize.io")
    size = int(response.headers["Content-Length"])

    with wrap_file(response, size) as file:
        for line in file:
            print(line.decode("utf-8"), end="")
            sleep(0.1)
```

----------------------------------------

TITLE: Safely Formatting Dynamic Strings with Rich Markup Escape
DESCRIPTION: This Python function demonstrates the safe way to handle dynamic string formatting with Rich by using `rich.markup.escape`. By applying `escape()` to the `name` parameter, any potential markup tags within the input string are neutralized, preventing unintended styling or markup injection when printed by `console.print`.
SOURCE: https://github.com/textualize/rich/blob/master/docs/source/markup.rst#_snippet_8

LANGUAGE: Python
CODE:
```
from rich.markup import escape
def greet(name):
    console.print(f"Hello {escape(name)}!")
```

----------------------------------------

TITLE: Rendering Markdown Content with Rich in Python
DESCRIPTION: This snippet demonstrates how to use the Rich library to render a multi-line Markdown string to the console. It initializes a `Console` object and a `Markdown` object, then prints the Markdown content, showcasing Rich's ability to format text and syntax highlight code blocks.
SOURCE: https://github.com/textualize/rich/blob/master/docs/source/markdown.rst#_snippet_0

LANGUAGE: Python
CODE:
```
MARKDOWN = """
# This is an h1

Rich can do a pretty *decent* job of rendering markdown.

1. This is a list item
2. This is another list item
"""
from rich.console import Console
from rich.markdown import Markdown

console = Console()
md = Markdown(MARKDOWN)
console.print(md)
```

----------------------------------------

TITLE: Configuring RichHandler for Traceback Formatting in Python
DESCRIPTION: This example illustrates how to configure `RichHandler` to use Rich's enhanced traceback formatting by setting `rich_tracebacks=True`. It demonstrates logging an exception with the improved traceback, providing more context.
SOURCE: https://github.com/textualize/rich/blob/master/docs/source/logging.rst#_snippet_3

LANGUAGE: Python
CODE:
```
import logging
from rich.logging import RichHandler

logging.basicConfig(
    level="NOTSET",
    format="%(message)s",
    datefmt="[%X]",
    handlers=[RichHandler(rich_tracebacks=True)]
)

log = logging.getLogger("rich")
try:
    print(1 / 0)
except Exception:
    log.exception("unable print!")
```

----------------------------------------

TITLE: Installing Rich Pretty Printing in Python REPL
DESCRIPTION: This Python code snippet installs Rich's pretty printing functionality into the current Python REPL session. After execution, Python data structures will be automatically pretty-printed with syntax highlighting for improved readability.
SOURCE: https://github.com/textualize/rich/blob/master/docs/source/introduction.rst#_snippet_5

LANGUAGE: Python
CODE:
```
from rich import pretty
pretty.install()
```

----------------------------------------

TITLE: String Prompt with Default Value using `rich.prompt.Prompt.ask` (Python)
DESCRIPTION: Shows how to assign a default value to `rich.prompt.Prompt.ask`. If the user submits an empty response, the specified default value is automatically returned.
SOURCE: https://github.com/textualize/rich/blob/master/docs/source/prompt.rst#_snippet_1

LANGUAGE: Python
CODE:
```
from rich.prompt import Prompt
name = Prompt.ask("Enter your name", default="Paul Atreides")
```

----------------------------------------

TITLE: Managing Multiple Progress Tasks with Context Manager
DESCRIPTION: This example shows how to manage multiple concurrent tasks using the `rich.progress.Progress` class as a context manager. It initializes three distinct tasks with different descriptions and colors, then continuously updates their progress using `advance` until all tasks are marked as finished. This approach ensures proper display start and stop.
SOURCE: https://github.com/textualize/rich/blob/master/docs/source/progress.rst#_snippet_2

LANGUAGE: Python
CODE:
```
import time

from rich.progress import Progress

with Progress() as progress:

    task1 = progress.add_task("[red]Downloading...", total=1000)
    task2 = progress.add_task("[green]Processing...", total=1000)
    task3 = progress.add_task("[cyan]Cooking...", total=1000)

    while not progress.finished:
        progress.update(task1, advance=0.5)
        progress.update(task2, advance=0.3)
        progress.update(task3, advance=0.9)
        time.sleep(0.02)
```

----------------------------------------

TITLE: Printing Basic Text with Rich Console (Python)
DESCRIPTION: This snippet shows how to use the `print` method of the `Console` object to output text to the terminal. It functions similarly to the built-in `print` function but includes Rich's word-wrapping capabilities.
SOURCE: https://github.com/textualize/rich/blob/master/README.md#_snippet_5

LANGUAGE: python
CODE:
```
console.print("Hello", "World!")
```

----------------------------------------

TITLE: Defining and Applying Custom Rich Style Themes in Python
DESCRIPTION: This snippet demonstrates how to create a custom `Theme` object with named styles (e.g., 'info', 'warning', 'danger') and apply it to a `Console` instance. It shows how to print text using these defined styles, either via the `style` parameter or inline markup, centralizing style definitions for easier maintenance.
SOURCE: https://github.com/textualize/rich/blob/master/docs/source/style.rst#_snippet_10

LANGUAGE: Python
CODE:
```
from rich.console import Console
from rich.theme import Theme
custom_theme = Theme({
    "info": "dim cyan",
    "warning": "magenta",
    "danger": "bold red"
})
console = Console(theme=custom_theme)
console.print("This is information", style="info")
console.print("[warning]The pod bay doors are locked[/warning]")
console.print("Something terrible happened!", style="danger")
```

----------------------------------------

TITLE: Yes/No Confirmation Prompt with `rich.prompt.Confirm.ask` (Python)
DESCRIPTION: Illustrates the use of `rich.prompt.Confirm.ask` for posing simple yes/no questions to the user. This specialized prompt returns a boolean value (`True` for yes, `False` for no) based on the user's response.
SOURCE: https://github.com/textualize/rich/blob/master/docs/source/prompt.rst#_snippet_4

LANGUAGE: Python
CODE:
```
from rich.prompt import Confirm
is_rich_great = Confirm.ask("Do you like rich?")
assert is_rich_great
```

----------------------------------------

TITLE: Customizing Console Output with `__rich__` Method (Python)
DESCRIPTION: This snippet demonstrates how to implement the `__rich__` method in a Python class. This method, accepting no arguments, allows an object to define its rich console representation by returning a renderable object, such as a string with console markup. When an instance of `MyObject` is printed, it will render as 'MyObject()' in bold cyan.
SOURCE: https://github.com/textualize/rich/blob/master/docs/source/protocol.rst#_snippet_0

LANGUAGE: Python
CODE:
```
class MyObject:
    def __rich__(self) -> str:
        return "[bold cyan]MyObject()"
```

----------------------------------------

TITLE: Inspecting a Rich Color Object in Python
DESCRIPTION: This snippet demonstrates how to use the `rich.inspect` function to generate a detailed report on a `rich.color.Color` object. It shows the object's attributes and methods, which is useful for debugging and understanding object structure. The `methods=True` argument ensures that callable methods are also included in the report.
SOURCE: https://github.com/textualize/rich/blob/master/docs/source/introduction.rst#_snippet_9

LANGUAGE: python
CODE:
```
from rich import inspect
from rich.color import Color
color = Color.parse("red")
inspect(color, methods=True)
```

----------------------------------------

TITLE: Displaying a Basic Status Message with Rich (Python)
DESCRIPTION: This Python snippet shows how to use `console.status` as a context manager. It displays "Working..." with a default spinner animation while the `do_work()` function (a placeholder for actual work) executes, automatically stopping the status display upon exiting the block.
SOURCE: https://github.com/textualize/rich/blob/master/docs/source/console.rst#_snippet_11

LANGUAGE: Python
CODE:
```
with console.status("Working..."):
    do_work()
```

----------------------------------------

TITLE: Displaying Progress with Rich Status Spinner in Python
DESCRIPTION: This snippet uses rich.console.Console.status to display a dynamic spinner animation and a message while a series of tasks are being processed. It's useful when exact progress calculation is difficult, providing visual feedback without blocking console interaction. The sleep(1) simulates work for each task.
SOURCE: https://github.com/textualize/rich/blob/master/README.md#_snippet_13

LANGUAGE: python
CODE:
```
from time import sleep
from rich.console import Console

console = Console()
tasks = [f"task {n}" for n in range(1, 11)]

with console.status("[bold green]Working on tasks...") as status:
    while tasks:
        task = tasks.pop(0)
        sleep(1)
        console.log(f"{task} complete")
```

----------------------------------------

TITLE: Setting Up Basic Rich Logger in Python
DESCRIPTION: This snippet demonstrates the basic setup for integrating Rich's `RichHandler` with Python's standard `logging` module. It configures a logger to output messages with Rich's formatting and colorization, showing a simple info message.
SOURCE: https://github.com/textualize/rich/blob/master/docs/source/logging.rst#_snippet_0

LANGUAGE: Python
CODE:
```
import logging
from rich.logging import RichHandler

FORMAT = "%(message)s"
logging.basicConfig(
    level="NOTSET", format=FORMAT, datefmt="[%X]", handlers=[RichHandler()]
)

log = logging.getLogger("rich")
log.info("Hello, World!")
```

----------------------------------------

TITLE: Applying Syntax Highlighting with Rich in Python
DESCRIPTION: This Python snippet utilizes rich.syntax.Syntax and the pygments library to apply syntax highlighting to a given Python code string. It configures the syntax object with the language ("python"), a theme ("monokai"), and line numbers, then prints the beautifully formatted code to the console.
SOURCE: https://github.com/textualize/rich/blob/master/README.md#_snippet_18

LANGUAGE: python
CODE:
```
from rich.console import Console
from rich.syntax import Syntax

my_code = '''
def iter_first_last(values: Iterable[T]) -> Iterable[Tuple[bool, bool, T]]:
    """Iterate and generate a tuple with a flag for first and last value."""
    iter_values = iter(values)
    try:
        previous_value = next(iter_values)
    except StopIteration:
        return
    first = True
    for value in iter_values:
        yield first, False, previous_value
        first = False
        previous_value = value
    yield first, True, previous_value
'''
syntax = Syntax(my_code, "python", theme="monokai", line_numbers=True)
console = Console()
console.print(syntax)
```

----------------------------------------

TITLE: Printing with Rich Console Markup and Pretty Formatting
DESCRIPTION: This Python code demonstrates using Rich's `print` function to output text with inline console markup for styling (e.g., italic red) and to pretty-print a Python object (`locals()`), making complex data structures more readable in the terminal.
SOURCE: https://github.com/textualize/rich/blob/master/docs/source/introduction.rst#_snippet_3

LANGUAGE: Python
CODE:
```
print("[italic red]Hello[/italic red] World!", locals())
```

----------------------------------------

TITLE: Applying Global Style with Rich Console (Python)
DESCRIPTION: This snippet illustrates how to apply a global style to the entire output of the `console.print` method using the `style` keyword argument. The example sets the text to be bold and red.
SOURCE: https://github.com/textualize/rich/blob/master/README.md#_snippet_6

LANGUAGE: python
CODE:
```
console.print("Hello", "World!", style="bold red")
```

----------------------------------------

TITLE: Writing Console Output to a File in Rich (Python)
DESCRIPTION: This snippet demonstrates how to redirect Rich console output to a file. It initializes a `Console` instance with a file object, allowing all subsequent `console` methods (like `console.rule`) to write to the specified file instead of the terminal. It also notes that `width` might need explicit setting.
SOURCE: https://github.com/textualize/rich/blob/master/docs/source/console.rst#_snippet_22

LANGUAGE: Python
CODE:
```
from rich.console import Console
from datetime import datetime

with open("report.txt", "wt") as report_file:
    console = Console(file=report_file)
    console.rule(f"Report Generated {datetime.now().ctime()}")
```

----------------------------------------

TITLE: Styling an Error Console in Rich Python
DESCRIPTION: This code builds upon the error console concept by also applying a visual style to it. By setting `stderr=True` and `style='bold red'`, all messages printed to `error_console` will appear in bold red, making error messages immediately distinct.
SOURCE: https://github.com/textualize/rich/blob/master/docs/source/console.rst#_snippet_21

LANGUAGE: Python
CODE:
```
error_console = Console(stderr=True, style="bold red")
```

----------------------------------------

TITLE: Pretty Printing JSON via Command Line (Bash)
DESCRIPTION: This snippet provides a command-line example for pretty-printing a JSON file (`cats.json`) using Rich's built-in module. This is useful for quick inspection of JSON data directly from the terminal.
SOURCE: https://github.com/textualize/rich/blob/master/docs/source/console.rst#_snippet_7

LANGUAGE: bash
CODE:
```
python -m rich.json cats.json
```

----------------------------------------

TITLE: Creating a Basic Rich Tree
DESCRIPTION: This snippet demonstrates the basic instantiation and printing of a `rich.tree.Tree` object. It initializes a tree with a root label 'Rich Tree' and then prints it to the console, showing only the root.
SOURCE: https://github.com/textualize/rich/blob/master/docs/source/tree.rst#_snippet_1

LANGUAGE: Python
CODE:
```
from rich.tree import Tree
from rich import print

tree = Tree("Rich Tree")
print(tree)
```

----------------------------------------

TITLE: Basic String Prompt with `rich.prompt.Prompt.ask` (Python)
DESCRIPTION: Illustrates the fundamental usage of `rich.prompt.Prompt.ask` to obtain a string input from the user. The prompt message can incorporate console markup and emoji codes for enhanced presentation.
SOURCE: https://github.com/textualize/rich/blob/master/docs/source/prompt.rst#_snippet_0

LANGUAGE: Python
CODE:
```
from rich.prompt import Prompt
name = Prompt.ask("Enter your name")
```

----------------------------------------

TITLE: String Prompt with Predefined Choices using `rich.prompt.Prompt.ask` (Python)
DESCRIPTION: Demonstrates how to restrict user input to a list of predefined choices using `rich.prompt.Prompt.ask`. The prompt will repeatedly ask for input until a valid choice from the list is provided, and a default value can also be set.
SOURCE: https://github.com/textualize/rich/blob/master/docs/source/prompt.rst#_snippet_2

LANGUAGE: Python
CODE:
```
from rich.prompt import Prompt
name = Prompt.ask("Enter your name", choices=["Paul", "Jessica", "Duncan"], default="Paul")
```

----------------------------------------

TITLE: Enabling Line Numbers for Rich Syntax Highlighting in Python
DESCRIPTION: This snippet demonstrates how to enable line numbers when highlighting code using `rich.syntax.Syntax.from_path`. By setting `line_numbers=True`, Rich will render a column displaying line numbers alongside the code. It builds upon the `from_path` constructor.
SOURCE: https://github.com/textualize/rich/blob/master/docs/source/syntax.rst#_snippet_2

LANGUAGE: python
CODE:
```
syntax = Syntax.from_path("syntax.py", line_numbers=True)
```

----------------------------------------

TITLE: Capturing Console Output with `StringIO` in Rich (Python)
DESCRIPTION: This snippet demonstrates an alternative method for capturing console output by setting the `Console`'s `file` argument to an `io.StringIO` object. After printing, the captured string can be retrieved from the `StringIO` buffer using `console.file.getvalue()`, which is recommended for unit testing.
SOURCE: https://github.com/textualize/rich/blob/master/docs/source/console.rst#_snippet_24

LANGUAGE: Python
CODE:
```
from io import StringIO
from rich.console import Console
console = Console(file=StringIO())
console.print("[bold red]Hello[/] World")
str_output = console.file.getvalue()
```

----------------------------------------

TITLE: Importing and Using Rich's pprint Method (Python)
DESCRIPTION: This snippet demonstrates how to import the `pprint` function from `rich.pretty` and then use it to pretty print the `locals()` dictionary, which contains all local symbols. This showcases the basic usage of the `pprint` method.
SOURCE: https://github.com/textualize/rich/blob/master/docs/source/pretty.rst#_snippet_1

LANGUAGE: Python
CODE:
```
from rich.pretty import pprint
pprint(locals())
```

----------------------------------------

TITLE: Getting User Input with Rich Console in Python
DESCRIPTION: This code shows how to use the `Console.input` method, which functions similarly to Python's built-in `input` but allows for rich-styled prompts. The example uses inline styling and an emoji for a colorful prompt.
SOURCE: https://github.com/textualize/rich/blob/master/docs/source/console.rst#_snippet_17

LANGUAGE: Python
CODE:
```
from rich.console import Console
console = Console()
console.input("What is [i]your[/i] [bold red]name[/]? :smiley: ")
```

----------------------------------------

TITLE: Using Rich Markup for Inline Styling (Python)
DESCRIPTION: This snippet demonstrates the use of Rich's special markup, similar to BBCode, for fine-grained inline styling within a printed string. It shows examples of bold, underline, and italic styles.
SOURCE: https://github.com/textualize/rich/blob/master/README.md#_snippet_7

LANGUAGE: python
CODE:
```
console.print("Where there is a [bold cyan]Will[/bold cyan] there [u]is[/u] a [i]way[/i].")
```

----------------------------------------

TITLE: Creating and Applying Styles with Rich Style Class
DESCRIPTION: Shows how to explicitly create a Style object with specific attributes (color, blink, bold) and then apply it to text using console.print, offering an alternative to style strings.
SOURCE: https://github.com/textualize/rich/blob/master/docs/source/style.rst#_snippet_7

LANGUAGE: Python
CODE:
```
from rich.style import Style
danger_style = Style(color="red", blink=True, bold=True)
console.print("Danger, Will Robinson!", style=danger_style)
```

----------------------------------------

TITLE: Pretty Printing JSON with Rich Console (Python)
DESCRIPTION: This example shows how to use the `console.print_json` method to pretty-print a JSON string to the terminal. This method automatically formats and styles the JSON for readability.
SOURCE: https://github.com/textualize/rich/blob/master/docs/source/console.rst#_snippet_4

LANGUAGE: python
CODE:
```
console.print_json('[false, true, null, "foo"]')
```

----------------------------------------

TITLE: Syntax Highlighting from File Path with Rich in Python
DESCRIPTION: This example shows how to use the `Syntax.from_path` alternative constructor to load and highlight code directly from a file. This method automatically detects the file type for highlighting. It requires `rich.console.Console` and `rich.syntax.Syntax`.
SOURCE: https://github.com/textualize/rich/blob/master/docs/source/syntax.rst#_snippet_1

LANGUAGE: python
CODE:
```
from rich.console import Console
from rich.syntax import Syntax

console = Console()
syntax = Syntax.from_path("syntax.py")
console.print(syntax)
```

----------------------------------------

TITLE: Basic Syntax Highlighting with Rich in Python
DESCRIPTION: This snippet demonstrates how to perform basic syntax highlighting using the `rich.syntax.Syntax` object. It reads code from a file, creates a `Syntax` object, and prints it to the console. It requires `rich.console.Console` and `rich.syntax.Syntax`.
SOURCE: https://github.com/textualize/rich/blob/master/docs/source/syntax.rst#_snippet_0

LANGUAGE: python
CODE:
```
from rich.console import Console
from rich.syntax import Syntax

console = Console()
with open("syntax.py", "rt") as code_file:
    syntax = Syntax(code_file.read(), "python")
console.print(syntax)
```

----------------------------------------

TITLE: Installing Rich with Jupyter Dependencies
DESCRIPTION: This command installs the Rich library along with additional dependencies specifically required for its integration and optimal use within Jupyter environments, ensuring full functionality in notebooks.
SOURCE: https://github.com/textualize/rich/blob/master/docs/source/introduction.rst#_snippet_1

LANGUAGE: Bash
CODE:
```
pip install "rich[jupyter]"
```

----------------------------------------

TITLE: Drawing a Styled Rule with Rich Console (Python)
DESCRIPTION: This code uses the `console.rule` method to draw a horizontal line with an optional title. The title "[bold red]Chapter 2" applies Rich's styling syntax to make the text bold and red, effectively creating a visual section divider.
SOURCE: https://github.com/textualize/rich/blob/master/docs/source/console.rst#_snippet_9

LANGUAGE: Python
CODE:
```
console.rule("[bold red]Chapter 2")
```

----------------------------------------

TITLE: Demonstrating Rich REPL Pretty Printing
DESCRIPTION: This Python code demonstrates the automatic pretty printing feature of Rich in the REPL. After `pretty.install()` is called, simple data structures like lists are automatically formatted and syntax-highlighted upon evaluation.
SOURCE: https://github.com/textualize/rich/blob/master/docs/source/introduction.rst#_snippet_6

LANGUAGE: Python
CODE:
```
["Rich and pretty", True]
```

----------------------------------------

TITLE: Unsafe Dynamic String Formatting with Rich
DESCRIPTION: This Python function demonstrates a potential vulnerability when dynamically formatting strings for Rich's `console.print`. Without proper escaping, malicious input for the `name` parameter could inject unwanted markup tags, leading to unexpected styling or behavior.
SOURCE: https://github.com/textualize/rich/blob/master/docs/source/markup.rst#_snippet_7

LANGUAGE: Python
CODE:
```
def greet(name):
    console.print(f"Hello {name}!")
```

----------------------------------------

TITLE: Creating a Transient Rich Progress Bar in Python
DESCRIPTION: This snippet demonstrates how to create a `rich.progress.Progress` bar that disappears from the terminal upon completion or exit. By setting `transient=True` in the constructor, the progress display is automatically removed, providing a cleaner terminal output. It shows adding a task and performing work.
SOURCE: https://github.com/textualize/rich/blob/master/docs/source/progress.rst#_snippet_4

LANGUAGE: Python
CODE:
```
with Progress(transient=True) as progress:
    task = progress.add_task("Working", total=100)
    do_work(task)
```

----------------------------------------

TITLE: Inserting Emojis in Rich Console (Python)
DESCRIPTION: This snippet demonstrates how to embed emojis directly into console output using Rich. By enclosing the emoji's shortcode name within two colons (e.g., `:smiley:`), the `console.print()` method will render the corresponding emoji character.
SOURCE: https://github.com/textualize/rich/blob/master/README.md#_snippet_10

LANGUAGE: python
CODE:
```
>>> console.print(":smiley: :vampire: :pile_of_poo: :thumbs_up: :raccoon:")
😃 🧛 💩 👍 🦝
```

----------------------------------------

TITLE: Creating a Grid Layout with Rich Table (Python)
DESCRIPTION: Illustrates using `rich.table.Table.grid` as a layout tool to position content. It creates a grid, adds two columns (one left-aligned, one right-aligned), and then adds a row with two pieces of text, effectively aligning them to the left and right edges of the terminal.
SOURCE: https://github.com/textualize/rich/blob/master/docs/source/tables.rst#_snippet_6

LANGUAGE: Python
CODE:
```
from rich import print
from rich.table import Table

grid = Table.grid(expand=True)
grid.add_column()
grid.add_column(justify="right")
grid.add_row("Raising shields", "[bold magenta]COMPLETED [green]:heavy_check_mark:")

print(grid)
```

----------------------------------------

TITLE: Basic Progress Tracking with rich.track
DESCRIPTION: This snippet demonstrates basic progress tracking using the `rich.progress.track` function. It iterates over a sequence, updating a single progress bar with a custom description, simulating work with a `time.sleep` call on each iteration. This is suitable for simple, single-task progress displays.
SOURCE: https://github.com/textualize/rich/blob/master/docs/source/progress.rst#_snippet_1

LANGUAGE: Python
CODE:
```
import time
from rich.progress import track

for i in track(range(20), description="Processing..."):
    time.sleep(1)  # Simulate work being done
```

----------------------------------------

TITLE: Dynamically Updating Live Display Renderable (Python)
DESCRIPTION: Illustrates how to change the entire renderable displayed by `rich.live.Live` on the fly using the `live.update()` method. It includes a helper function `generate_table` that creates a new `Table` with random data, demonstrating a more dynamic display.
SOURCE: https://github.com/textualize/rich/blob/master/docs/source/live.rst#_snippet_1

LANGUAGE: Python
CODE:
```
import random
import time

from rich.live import Live
from rich.table import Table


def generate_table() -> Table:
    """Make a new table."""
    table = Table()
    table.add_column("ID")
    table.add_column("Value")
    table.add_column("Status")

    for row in range(random.randint(2, 6)):
        value = random.random() * 100
        table.add_row(
            f"{row}", f"{value:3.2f}", "[red]ERROR" if value < 50 else "[green]SUCCESS"
        )
    return table


with Live(generate_table(), refresh_per_second=4) as live:
    for _ in range(40):
        time.sleep(0.4)
        live.update(generate_table())
```

----------------------------------------

TITLE: Styling Console Output with Rich Python
DESCRIPTION: This snippet demonstrates how to apply a global style to all output from a Rich Console instance by setting the `style` attribute during initialization. The example sets a 'white on blue' background and foreground style for printed text.
SOURCE: https://github.com/textualize/rich/blob/master/docs/source/console.rst#_snippet_16

LANGUAGE: Python
CODE:
```
from rich.console import Console
blue_console = Console(style="white on blue")
blue_console.print("I'm blue. Da ba dee da ba di.")
```

----------------------------------------

TITLE: Initializing a Rich Table with a Specific Box Style (Python)
DESCRIPTION: Demonstrates how to create a `rich.table.Table` instance, setting a title and a specific box style (`box.MINIMAL_DOUBLE_HEAD`) for its borders. This snippet requires the `box` module from `rich`.
SOURCE: https://github.com/textualize/rich/blob/master/docs/source/tables.rst#_snippet_1

LANGUAGE: Python
CODE:
```
from rich import box
table = Table(title="Star Wars Movies", box=box.MINIMAL_DOUBLE_HEAD)
```

----------------------------------------

TITLE: Appending Styled Text with rich.text.Text.append (Python)
DESCRIPTION: This example shows how to build styled text incrementally by appending strings and optional styles to a `Text` object using the `append` method. It appends 'Hello' with 'bold magenta' style, followed by ' World!' without a specific style, and then prints the combined text to the console.
SOURCE: https://github.com/textualize/rich/blob/master/docs/source/text.rst#_snippet_1

LANGUAGE: Python
CODE:
```
text = Text()
text.append("Hello", style="bold magenta")
text.append(" World!")
console.print(text)
```

----------------------------------------

TITLE: Customizing Rich Repr with __rich_repr__ and Typing in Python
DESCRIPTION: This Python snippet demonstrates how to manually implement the `__rich_repr__` method within a class to control how Rich formats its instances. It uses `yield` statements to specify positional arguments, keyword arguments, and keyword arguments with default values that can be omitted, leveraging `rich.repr.Result` for type hinting and error checking.
SOURCE: https://github.com/textualize/rich/blob/master/docs/source/pretty.rst#_snippet_13

LANGUAGE: Python
CODE:
```
import rich.repr


class Bird:
    def __init__(self, name, eats=None, fly=True, extinct=False):
        self.name = name
        self.eats = list(eats) if eats else []
        self.fly = fly
        self.extinct = extinct

    def __rich_repr__(self) -> rich.repr.Result:
        yield self.name
        yield "eats", self.eats
        yield "fly", self.fly, True
        yield "extinct", self.extinct, False
```

----------------------------------------

TITLE: Setting Table Box Style with Rich
DESCRIPTION: This snippet demonstrates how to import and apply a predefined box style from `rich.box` to a `Table` object. It shows the basic syntax for setting the `box` parameter during table initialization.
SOURCE: https://github.com/textualize/rich/blob/master/docs/source/appendix/box.rst#_snippet_0

LANGUAGE: Python
CODE:
```
from rich import box
table = Table(box=box.SQUARE)
```

----------------------------------------

TITLE: Case-Insensitive String Prompt with Choices using `rich.prompt.Prompt.ask` (Python)
DESCRIPTION: Expands on choice-based prompts by enabling case-insensitive matching for user input. Setting `case_sensitive=False` allows the user to enter choices without strict adherence to the original casing (e.g., 'paul' will match 'Paul').
SOURCE: https://github.com/textualize/rich/blob/master/docs/source/prompt.rst#_snippet_3

LANGUAGE: Python
CODE:
```
from rich.prompt import Prompt
name = Prompt.ask("Enter your name", choices=["Paul", "Jessica", "Duncan"], default="Paul", case_sensitive=False)
```

----------------------------------------

TITLE: Importing Rich Print with Alias
DESCRIPTION: This Python statement imports the `print` function from the `rich` library and assigns it the alias `rprint`. This approach is useful to avoid shadowing Python's built-in `print` function while still utilizing Rich's enhanced output capabilities.
SOURCE: https://github.com/textualize/rich/blob/master/docs/source/introduction.rst#_snippet_4

LANGUAGE: Python
CODE:
```
from rich import print as rprint
```

----------------------------------------

TITLE: Suppressing Framework Frames in Rich Tracebacks (Python)
DESCRIPTION: This snippet shows how to exclude specific framework code from Rich tracebacks by using the `tracebacks_suppress` argument in `RichHandler`. It demonstrates suppressing `click` module frames, resulting in cleaner tracebacks focused on application code.
SOURCE: https://github.com/textualize/rich/blob/master/docs/source/logging.rst#_snippet_4

LANGUAGE: Python
CODE:
```
import click
import logging
from rich.logging import RichHandler

logging.basicConfig(
    level="NOTSET",
    format="%(message)s",
    datefmt="[%X]",
    handlers=[RichHandler(rich_tracebacks=True, tracebacks_suppress=[click])]
)
```

----------------------------------------

TITLE: Expanding All Data Structures with Rich pprint (Python)
DESCRIPTION: This example shows how to use the `expand_all=True` argument with `rich.pretty.pprint` to force the full expansion of data structures, preventing Rich from trying to fit them on a single line. This is useful for deeply nested or complex objects where full visibility is desired.
SOURCE: https://github.com/textualize/rich/blob/master/docs/source/pretty.rst#_snippet_2

LANGUAGE: Python
CODE:
```
pprint(["eggs", "ham"], expand_all=True)
```

----------------------------------------

TITLE: Demonstrating Text Overflow Methods with Rich Console (Python)
DESCRIPTION: This code initializes a `Console` with a narrow width to force text overflow. It then iterates through different `overflow` methods ("fold", "crop", "ellipsis") for `console.print`, demonstrating how Rich handles text that exceeds the available display space by either wrapping, truncating, or adding an ellipsis.
SOURCE: https://github.com/textualize/rich/blob/master/docs/source/console.rst#_snippet_15

LANGUAGE: Python
CODE:
```
from typing import List
from rich.console import Console, OverflowMethod

console = Console(width=14)
supercali = "supercalifragilisticexpialidocious"

overflow_methods: List[OverflowMethod] = ["fold", "crop", "ellipsis"]
for overflow in overflow_methods:
    console.rule(overflow)
    console.print(supercali, overflow=overflow, style="bold blue")
    console.print()
```

----------------------------------------

TITLE: Adding Custom Columns to Rich Progress Bar with Defaults in Python
DESCRIPTION: This snippet demonstrates how to combine custom columns with the default set of columns in a `rich.progress.Progress` bar. It uses `*Progress.get_default_columns()` to unpack the standard columns, allowing for the insertion of additional columns like `SpinnerColumn` and `TimeElapsedColumn` at specific positions.
SOURCE: https://github.com/textualize/rich/blob/master/docs/source/progress.rst#_snippet_6

LANGUAGE: Python
CODE:
```
progress = Progress(
    SpinnerColumn(),
    *Progress.get_default_columns(),
    TimeElapsedColumn(),
)
```

----------------------------------------

TITLE: Parsing Style Definitions with Rich Style.parse
DESCRIPTION: Illustrates two equivalent ways to create a Style object: directly instantiating it with keyword arguments or parsing a style definition string using the Style.parse method.
SOURCE: https://github.com/textualize/rich/blob/master/docs/source/style.rst#_snippet_9

LANGUAGE: Python
CODE:
```
style = Style(color="magenta", bgcolor="yellow", italic=True)
```

LANGUAGE: Python
CODE:
```
style = Style.parse("italic magenta on yellow")
```

----------------------------------------

TITLE: Logging Rich JSON Object (Python)
DESCRIPTION: This snippet demonstrates logging a `JSON` object from the `rich.json` module. By wrapping a JSON string in a `JSON` object, it can be passed to `console.log` for formatted and debug-enhanced output.
SOURCE: https://github.com/textualize/rich/blob/master/docs/source/console.rst#_snippet_5

LANGUAGE: python
CODE:
```
from rich.json import JSON
console.log(JSON('["foo", "bar"]'))
```

----------------------------------------

TITLE: Stylizing Text with rich.text.Text.stylize (Python)
DESCRIPTION: This snippet demonstrates how to apply a style to a specific range of characters within a `Text` object using the `stylize` method. It initializes a `Text` object, applies 'bold magenta' style from index 0 to 6, and then prints the styled text to the console. The `stylize` method modifies the `Text` object in-place.
SOURCE: https://github.com/textualize/rich/blob/master/docs/source/text.rst#_snippet_0

LANGUAGE: Python
CODE:
```
from rich.console import Console
from rich.text import Text

console = Console()
text = Text("Hello, World!")
text.stylize("bold magenta", 0, 6)
console.print(text)
```

----------------------------------------

TITLE: Adding Columns to Rich Table with Column Objects (Python)
DESCRIPTION: Demonstrates how to add columns to a `rich.table.Table` using `rich.table.Column` objects. This allows for more detailed configuration of individual columns, such as setting the header text and justification (`justify="right"`).
SOURCE: https://github.com/textualize/rich/blob/master/docs/source/tables.rst#_snippet_4

LANGUAGE: Python
CODE:
```
from rich.table import Column, Table
table = Table(
    "Released",
    "Title",
    Column(header="Box Office", justify="right"),
    title="Star Wars Movies"
)
```

----------------------------------------

TITLE: Assembling Styled Text with rich.text.Text.assemble (Python)
DESCRIPTION: This example illustrates how to construct a `Text` object from multiple parts using the `assemble` class method. It combines a tuple of text and style ('Hello', 'bold magenta') with a plain string (', World!') to create a single `Text` instance, which is then printed to the console. This method provides a concise way to build complex styled text.
SOURCE: https://github.com/textualize/rich/blob/master/docs/source/text.rst#_snippet_3

LANGUAGE: Python
CODE:
```
text = Text.assemble(("Hello", "bold magenta"), ", World!")
console.print(text)
```

----------------------------------------

TITLE: Displaying Progress While Reading File with Rich in Python
DESCRIPTION: This example illustrates how to use `rich.progress.open` to automatically display a progress bar while reading a file. It wraps the file opening operation, making it suitable for scenarios where the reading logic cannot be easily modified, such as loading a JSON file. The progress bar is managed automatically by Rich.
SOURCE: https://github.com/textualize/rich/blob/master/docs/source/progress.rst#_snippet_10

LANGUAGE: Python
CODE:
```
import json
    import rich.progress

    with rich.progress.open("data.json", "rb") as file:
        data = json.load(file)
    print(data)
```

----------------------------------------

TITLE: Demonstrating Rich Renderables in REPL
DESCRIPTION: This Python code snippet illustrates how to create and display a Rich `Panel` renderable directly within the REPL. It showcases Rich's ability to render complex, styled components for visual output.
SOURCE: https://github.com/textualize/rich/blob/master/docs/source/introduction.rst#_snippet_7

LANGUAGE: Python
CODE:
```
from rich.panel import Panel
Panel.fit("[bold yellow]Hi, I'm a Panel", border_style="red")
```

----------------------------------------

TITLE: Customizing Rich Progress Bar Columns in Python
DESCRIPTION: This snippet demonstrates how to customize the column widths of a Rich `Progress` instance. It uses `TextColumn` and `BarColumn` with `Column(ratio=...)` to allocate specific proportions of the terminal width to the task description and the progress bar, respectively. The example simulates a task loop with a delay.
SOURCE: https://github.com/textualize/rich/blob/master/docs/source/progress.rst#_snippet_7

LANGUAGE: Python
CODE:
```
from time import sleep

    from rich.table import Column
    from rich.progress import Progress, BarColumn, TextColumn

    text_column = TextColumn("{task.description}", table_column=Column(ratio=1))
    bar_column = BarColumn(bar_width=None, table_column=Column(ratio=2))
    progress = Progress(text_column, bar_column, expand=True)

    with progress:
        for n in progress.track(range(100)):
            progress.print(n)
            sleep(0.1)
```

----------------------------------------

TITLE: Demonstrating Text Justification with Rich Console (Python)
DESCRIPTION: This snippet initializes a `Console` with a fixed width and then demonstrates various text justification options ("default", "left", "center", "right") using `console.print`. It also applies a background style to clearly highlight the effect of each justification type.
SOURCE: https://github.com/textualize/rich/blob/master/docs/source/console.rst#_snippet_14

LANGUAGE: Python
CODE:
```
from rich.console import Console

console = Console(width=20)

style = "bold white on blue"
console.print("Rich", style=style)
console.print("Rich", style=style, justify="left")
console.print("Rich", style=style, justify="center")
console.print("Rich", style=style, justify="right")
```

----------------------------------------

TITLE: Creating Hyperlinks with Rich Console Markup
DESCRIPTION: This Python snippet illustrates how to embed clickable hyperlinks within text using Rich console markup. The `[link=URL]text[/link]` syntax creates a hyperlink, making the specified 'text' clickable in terminals that support hyperlinks, directing the user to the provided URL.
SOURCE: https://github.com/textualize/rich/blob/master/docs/source/markup.rst#_snippet_5

LANGUAGE: Python
CODE:
```
print("Visit my [link=https://www.willmcgugan.com]blog[/link]!")
```

----------------------------------------

TITLE: Escaping Markup Tags in Rich Print
DESCRIPTION: This Python snippet demonstrates how to escape potential Rich console markup tags using a backslash (`\`). By preceding `[bar]` with `\`, Rich treats it as literal text rather than a style tag, ensuring that strings containing bracketed content are printed as intended without being interpreted as markup.
SOURCE: https://github.com/textualize/rich/blob/master/docs/source/markup.rst#_snippet_6

LANGUAGE: Python
CODE:
```
>>> from rich import print
>>> print(r"foo\\[bar]")
```

----------------------------------------

TITLE: Embedding Pretty Printed Data in a Rich Panel (Python)
DESCRIPTION: This code demonstrates how to use the `rich.pretty.Pretty` class to create a renderable object from pretty-printed data. This `Pretty` object is then embedded within a `rich.panel.Panel` and printed, showcasing how to integrate pretty output into more complex Rich layouts.
SOURCE: https://github.com/textualize/rich/blob/master/docs/source/pretty.rst#_snippet_5

LANGUAGE: Python
CODE:
```
from rich import print
from rich.pretty import Pretty
from rich.panel import Panel

pretty = Pretty(locals())
panel = Panel(pretty)
print(panel)
```

----------------------------------------

TITLE: Declaring Python Package Dependencies
DESCRIPTION: This snippet demonstrates how to declare Python package dependencies with exact version pinning, a common practice in `requirements.txt` files. This ensures environment reproducibility and prevents unexpected behavior due to package updates.
SOURCE: https://github.com/textualize/rich/blob/master/docs/requirements.txt#_snippet_0

LANGUAGE: Python
CODE:
```
alabaster==1.0.0
Sphinx==8.2.3
sphinx-rtd-theme==3.0.2
sphinx-copybutton==0.5.2
```

----------------------------------------

TITLE: Capturing Console Output with `capture()` in Rich (Python)
DESCRIPTION: This example shows how to capture console output into a string using the `console.capture()` context manager. It prints formatted text within the context, and upon exiting, retrieves the rendered string using `capture.get()`, useful for testing or programmatic processing.
SOURCE: https://github.com/textualize/rich/blob/master/docs/source/console.rst#_snippet_23

LANGUAGE: Python
CODE:
```
from rich.console import Console
console = Console()
with console.capture() as capture:
    console.print("[bold red]Hello[/] World")
str_output = capture.get()
```

----------------------------------------

TITLE: Applying Foreground Color (Magenta) in Rich Python
DESCRIPTION: Demonstrates how to apply a basic foreground color (magenta) to text using a style string in Rich's console.print method.
SOURCE: https://github.com/textualize/rich/blob/master/docs/source/style.rst#_snippet_0

LANGUAGE: Python
CODE:
```
console.print("Hello", style="magenta")
```

----------------------------------------

TITLE: Combining Multiple Style Attributes and Colors in Rich Python
DESCRIPTION: Shows how to combine various style attributes (blink, bold, underline) and colors (red foreground, white background) within a single style string for console.print.
SOURCE: https://github.com/textualize/rich/blob/master/docs/source/style.rst#_snippet_4

LANGUAGE: Python
CODE:
```
console.print("Danger, Will Robinson!", style="blink bold red underline on white")
```

----------------------------------------

TITLE: Applying Foreground and Background Colors in Rich Python
DESCRIPTION: Explains how to set both foreground (red) and background (white) colors simultaneously using the "on" keyword within a style string for console.print.
SOURCE: https://github.com/textualize/rich/blob/master/docs/source/style.rst#_snippet_3

LANGUAGE: Python
CODE:
```
console.print("DANGER!", style="red on white")
```

----------------------------------------

TITLE: Updating Rich Layout Content in Python
DESCRIPTION: This snippet illustrates how to dynamically change the content of a specific Rich Layout region using the `update` method. This allows for real-time modification of displayed text or other renderables within a defined layout area, followed by printing the updated layout.
SOURCE: https://github.com/textualize/rich/blob/master/docs/source/layout.rst#_snippet_5

LANGUAGE: python
CODE:
```
layout["left"].update(
    "The mystery of life isn't a problem to solve, but a reality to experience."
)
print(layout)
```

----------------------------------------

TITLE: Paging Long Console Output in Rich (Python)
DESCRIPTION: This example illustrates how to display long console output using an external pager application via the `console.pager()` context manager. Content printed within this context, such as a test card, will be sent to the system's default pager, allowing the user to scroll through it.
SOURCE: https://github.com/textualize/rich/blob/master/docs/source/console.rst#_snippet_25

LANGUAGE: Python
CODE:
```
from rich.__main__ import make_test_card
from rich.console import Console

console = Console()
with console.pager():
    console.print(make_test_card())
```

----------------------------------------

TITLE: Splitting a Rich Layout into Columns in Python
DESCRIPTION: This Python snippet demonstrates how to divide an existing `Layout` object vertically into two sub-layouts using the `split_column` method. Each new sub-layout is given a `name` attribute for later reference, resulting in the terminal screen being split into two equal-sized portions, one above the other.
SOURCE: https://github.com/textualize/rich/blob/master/docs/source/layout.rst#_snippet_2

LANGUAGE: python
CODE:
```
layout.split_column(
    Layout(name="upper"),
    Layout(name="lower")
)
print(layout)
```

----------------------------------------

TITLE: Creating an Error Console in Rich Python
DESCRIPTION: This snippet shows how to create a dedicated console for error messages by setting the `stderr` argument to `True` during initialization. This directs the console's output to `sys.stderr` instead of the default `sys.stdout`, separating error logs from regular output.
SOURCE: https://github.com/textualize/rich/blob/master/docs/source/console.rst#_snippet_20

LANGUAGE: Python
CODE:
```
from rich.console import Console
error_console = Console(stderr=True)
```

----------------------------------------

TITLE: Implementing Rich Repr Protocol for Custom Class (Python)
DESCRIPTION: This method implements the `__rich_repr__` protocol for a custom class. It yields attributes as tuples (name, value, default) or just values, allowing Rich to format the object's representation more concisely and intelligently, omitting default values and handling line wrapping effectively.
SOURCE: https://github.com/textualize/rich/blob/master/docs/source/pretty.rst#_snippet_8

LANGUAGE: Python
CODE:
```
def __rich_repr__(self):
    yield self.name
    yield "eats", self.eats
    yield "fly", self.fly, True
    yield "extinct", self.extinct, False
```

----------------------------------------

TITLE: Displaying Directory Contents in Rich Columns in Python
DESCRIPTION: This Python snippet uses rich.columns.Columns to display a directory listing in a columnar format, similar to the ls command. It takes a directory path as a command-line argument, lists its contents, and then prints them neatly arranged in columns with optimal width.
SOURCE: https://github.com/textualize/rich/blob/master/README.md#_snippet_16

LANGUAGE: python
CODE:
```
import os
import sys

from rich import print
from rich.columns import Columns

directory = os.listdir(sys.argv[1])
print(Columns(directory))
```

----------------------------------------

TITLE: Using Rich Text with Panel and Justification (Python)
DESCRIPTION: This snippet demonstrates integrating a `Text` object with a `Panel` to control text rendering within other Rich renderables. It creates a `Text` object with right justification and embeds it within a `Panel`, then prints the `Panel`. This shows how `Text` attributes like `justify` can influence the display of content in containers.
SOURCE: https://github.com/textualize/rich/blob/master/docs/source/text.rst#_snippet_4

LANGUAGE: Python
CODE:
```
from rich import print
from rich.panel import Panel
from rich.text import Text
panel = Panel(Text("Hello", justify="right"))
print(panel)
```

----------------------------------------

TITLE: Nesting Branches in a Rich Tree
DESCRIPTION: This snippet demonstrates creating nested branches within a Rich Tree. It adds a 'baz' branch, then uses the returned `Tree` instance to chain `add` calls, creating 'Red', 'Green', and 'Blue' as sub-branches of 'baz', showcasing multi-level hierarchy and Rich's console markup.
SOURCE: https://github.com/textualize/rich/blob/master/docs/source/tree.rst#_snippet_3

LANGUAGE: Python
CODE:
```
baz_tree = tree.add("baz")
baz_tree.add("[red]Red").add("[green]Green").add("[blue]Blue")
print(tree)
```

----------------------------------------

TITLE: Setting Fixed Size for Rich Layout - Python
DESCRIPTION: This snippet demonstrates how to set a fixed size for a specific layout region in Rich. It assigns a value of 10 to the 'size' attribute of the 'upper' layout, making it occupy exactly 10 rows (or characters if horizontal). The layout is then printed to show the effect.
SOURCE: https://github.com/textualize/rich/blob/master/docs/source/layout.rst#_snippet_6

LANGUAGE: Python
CODE:
```
layout["upper"].size = 10
print(layout)
```

----------------------------------------

TITLE: Splitting Rich Layouts with Panels in Python
DESCRIPTION: This snippet demonstrates how to divide an existing Rich Layout region into multiple sub-layouts using the `split` method. It shows how to embed `Panel` renderables within these new layout sections, effectively creating a multi-panel display.
SOURCE: https://github.com/textualize/rich/blob/master/docs/source/layout.rst#_snippet_4

LANGUAGE: python
CODE:
```
from rich.panel import Panel

layout["right"].split(
    Layout(Panel("Hello")),
    Layout(Panel("World!"))
)
```

----------------------------------------

TITLE: Creating a Rich Panel that Fits Content
DESCRIPTION: This example shows how to create a `rich.panel.Panel` that automatically adjusts its width to fit its content using the `Panel.fit()` class method. This prevents the panel from expanding to the full terminal width, making it more compact.
SOURCE: https://github.com/textualize/rich/blob/master/docs/source/panel.rst#_snippet_1

LANGUAGE: Python
CODE:
```
from rich import print
from rich.panel import Panel
print(Panel.fit("Hello, [red]World!"))
```

----------------------------------------

TITLE: Splitting a Sub-Layout into Rows in Python
DESCRIPTION: This Python snippet illustrates how to further subdivide a specific named sub-layout (accessed via `layout["lower"]`) horizontally into two new sub-layouts using the `split_row` method. This action creates a more complex layout structure, dividing the previously defined 'lower' section into 'left' and 'right' quarters.
SOURCE: https://github.com/textualize/rich/blob/master/docs/source/layout.rst#_snippet_3

LANGUAGE: python
CODE:
```
layout["lower"].split_row(
    Layout(name="left"),
    Layout(name="right"),
)
print(layout)
```

----------------------------------------

TITLE: Enabling Console Markup for Rich Logs in Python
DESCRIPTION: This example shows how to enable Rich's console markup for a specific log message by passing `markup=True` in the `extra` argument. This allows for rich text formatting within the log message itself.
SOURCE: https://github.com/textualize/rich/blob/master/docs/source/logging.rst#_snippet_1

LANGUAGE: Python
CODE:
```
log.error("[bold red blink]Server is shutting down![/]", extra={"markup": True})
```

----------------------------------------

TITLE: Integrating External Rich Console with Progress in Python
DESCRIPTION: This snippet demonstrates how to integrate an existing `Console` object with a Rich `Progress` instance by passing it to the `Progress` constructor. This allows all console output, including progress updates and custom messages, to be managed by a single, shared console instance. `my_console` and `do_work` are placeholders.
SOURCE: https://github.com/textualize/rich/blob/master/docs/source/progress.rst#_snippet_9

LANGUAGE: Python
CODE:
```
from my_project import my_console

    with Progress(console=my_console) as progress:
        my_console.print("[bold blue]Starting work!")
        do_work(progress)
```

----------------------------------------

TITLE: Adding Branches to a Rich Tree
DESCRIPTION: This code extends an existing `rich.tree.Tree` instance by adding two new top-level branches, 'foo' and 'bar', to the root. The `add` method appends new nodes, making the tree display with guide lines connecting them.
SOURCE: https://github.com/textualize/rich/blob/master/docs/source/tree.rst#_snippet_2

LANGUAGE: Python
CODE:
```
tree.add("foo")
tree.add("bar")
print(tree)
```

----------------------------------------

TITLE: Applying Granular Padding (Top/Bottom, Left/Right) with Rich Python
DESCRIPTION: This example illustrates how to apply granular padding using a tuple of two values. The first value (2) sets the top and bottom padding, and the second value (4) sets the left and right padding, effectively adding two blank lines vertically and four spaces horizontally around the 'Hello' text.
SOURCE: https://github.com/textualize/rich/blob/master/docs/source/padding.rst#_snippet_1

LANGUAGE: python
CODE:
```
from rich import print
from rich.padding import Padding
test = Padding("Hello", (2, 4))
print(test)
```

----------------------------------------

TITLE: Managing Multiple Progress Tasks Manually (No Context Manager)
DESCRIPTION: This snippet demonstrates how to use the `rich.progress.Progress` class without a context manager. It manually calls `progress.start()` to begin the display and `progress.stop()` in a `finally` block to ensure the display is properly terminated, even if errors occur. It manages multiple tasks similarly to the context manager example, updating their progress iteratively.
SOURCE: https://github.com/textualize/rich/blob/master/docs/source/progress.rst#_snippet_3

LANGUAGE: Python
CODE:
```
import time

from rich.progress import Progress

progress = Progress()
progress.start()
try:
    task1 = progress.add_task("[red]Downloading...", total=1000)
    task2 = progress.add_task("[green]Processing...", total=1000)
    task3 = progress.add_task("[cyan]Cooking...", total=1000)

    while not progress.finished:
        progress.update(task1, advance=0.5)
        progress.update(task2, advance=0.3)
        progress.update(task3, advance=0.9)
        time.sleep(0.02)
finally:
    progress.stop()
```

----------------------------------------

TITLE: Adding Columns to Rich Table by Positional Arguments (Python)
DESCRIPTION: Illustrates how to initialize a `rich.table.Table` by directly specifying column headers as positional arguments in the constructor. This method is suitable for simple column definitions where only the header text is needed.
SOURCE: https://github.com/textualize/rich/blob/master/docs/source/tables.rst#_snippet_3

LANGUAGE: Python
CODE:
```
table = Table("Released", "Title", "Box Office", title="Star Wars Movies")
```

----------------------------------------

TITLE: Printing Above Rich Progress Display in Python
DESCRIPTION: This example shows how to print messages above the active Rich progress bar using the `progress.console` object. It adds a task and then, within the task loop, prints status updates to the console, ensuring they appear without disrupting the progress display. `run_job(job)` is a placeholder for actual work.
SOURCE: https://github.com/textualize/rich/blob/master/docs/source/progress.rst#_snippet_8

LANGUAGE: Python
CODE:
```
with Progress() as progress:
        task = progress.add_task("twiddling thumbs", total=10)
        for job in range(10):
            progress.console.print(f"Working on job #{job}")
            run_job(job)
            progress.advance(task)
```

----------------------------------------

TITLE: Adding Hyperlinks to Text in Rich Python
DESCRIPTION: Illustrates how to embed a clickable hyperlink within styled text by including the link attribute followed by the URL in the style string for console.print.
SOURCE: https://github.com/textualize/rich/blob/master/docs/source/style.rst#_snippet_6

LANGUAGE: Python
CODE:
```
console.print("Google", style="link https://google.com")
```

----------------------------------------

TITLE: Suppressing Framework Frames in Rich Tracebacks
DESCRIPTION: This example demonstrates how to configure the Rich traceback handler to suppress frames originating from specific modules or frameworks, such as 'click'. By passing a list of modules to the `suppress` argument, only relevant application code frames are shown in the traceback, improving clarity.
SOURCE: https://github.com/textualize/rich/blob/master/docs/source/traceback.rst#_snippet_5

LANGUAGE: Python
CODE:
```
import click
from rich.traceback import install
install(suppress=[click])
```

----------------------------------------

TITLE: Handling Empty Tables in Rich (Python)
DESCRIPTION: Shows how to conditionally print a `rich.table.Table` based on whether it contains any columns. If the table has columns, it's printed; otherwise, a custom message indicating no data is displayed. This prevents printing a blank line for empty tables.
SOURCE: https://github.com/textualize/rich/blob/master/docs/source/tables.rst#_snippet_2

LANGUAGE: Python
CODE:
```
if table.columns:
    print(table)
else:
    print("[i]No data...[/i]")
```

----------------------------------------

TITLE: Applying Truecolor (Hex and RGB) in Rich Python
DESCRIPTION: Illustrates how to use CSS-like hex (#af00ff) and RGB (rgb(175,0,255)) syntax to apply truecolors to text with console.print, enabling access to 16.7 million colors.
SOURCE: https://github.com/textualize/rich/blob/master/docs/source/style.rst#_snippet_2

LANGUAGE: Python
CODE:
```
console.print("Hello", style="#af00ff")
```

LANGUAGE: Python
CODE:
```
console.print("Hello", style="rgb(175,0,255)")
```

----------------------------------------

TITLE: Hiding a Rich Layout - Python
DESCRIPTION: This code demonstrates how to make a specific layout region invisible. By setting the 'visible' attribute of the 'upper' layout to False, it is hidden, and other visible layouts expand to fill the space. The layout is then printed to reflect the change.
SOURCE: https://github.com/textualize/rich/blob/master/docs/source/layout.rst#_snippet_9

LANGUAGE: Python
CODE:
```
layout["upper"].visible = False
print(layout)
```

----------------------------------------

TITLE: Setting Flexible Ratio for Rich Layout - Python
DESCRIPTION: This example shows how to make a layout flexible using the 'ratio' attribute. It first resets the 'size' to None, then sets the 'ratio' of the 'upper' layout to 2. This causes the 'upper' layout to take up two-thirds of the available space relative to other layouts with a default ratio of 1.
SOURCE: https://github.com/textualize/rich/blob/master/docs/source/layout.rst#_snippet_7

LANGUAGE: Python
CODE:
```
layout["upper"].size = None
layout["upper"].ratio = 2
print(layout)
```

----------------------------------------

TITLE: Grouping Panels with rich.console.group Decorator (Python)
DESCRIPTION: This snippet illustrates using the `rich.console.group` decorator to dynamically create a group of renderables from an iterator. This approach is more flexible for a larger or dynamic number of renderables compared to directly instantiating `Group`. It requires importing `print`, `group`, and `Panel` from the `rich` library.
SOURCE: https://github.com/textualize/rich/blob/master/docs/source/group.rst#_snippet_1

LANGUAGE: python
CODE:
```
from rich import print
from rich.console import group
from rich.panel import Panel

@group()
def get_panels():
    yield Panel("Hello", style="on blue")
    yield Panel("World", style="on red")

print(Panel(get_panels()))
```

----------------------------------------

TITLE: Loading Rich IPython Extension
DESCRIPTION: This IPython magic command loads the Rich extension within an IPython environment. This extension automatically enables Rich's pretty printing and pretty tracebacks, enhancing the interactive experience.
SOURCE: https://github.com/textualize/rich/blob/master/docs/source/introduction.rst#_snippet_8

LANGUAGE: IPython
CODE:
```
%load_ext rich
```

----------------------------------------

TITLE: Initializing and Printing a Basic Rich Layout in Python
DESCRIPTION: This Python snippet shows the fundamental steps to create and display a `Layout` object. It imports the necessary `print` function from `rich` and the `Layout` class, then instantiates a `Layout` object and prints it to the console, which initially draws a placeholder box.
SOURCE: https://github.com/textualize/rich/blob/master/docs/source/layout.rst#_snippet_1

LANGUAGE: python
CODE:
```
from rich import print
from rich.layout import Layout

layout = Layout()
print(layout)
```

----------------------------------------

TITLE: Enabling Output Recording for Export in Rich Python
DESCRIPTION: This snippet initializes a Rich Console instance with `record=True`, which is a prerequisite for exporting console output. Setting `record` to true tells Rich to save a copy of all data printed or logged to the console, making it available for later export.
SOURCE: https://github.com/textualize/rich/blob/master/docs/source/console.rst#_snippet_18

LANGUAGE: Python
CODE:
```
from rich.console import Console
console = Console(record=True)
```

----------------------------------------

TITLE: Example INI Configuration for Rich Style Themes
DESCRIPTION: This snippet provides an example of an external configuration file in INI format that defines custom Rich styles. These styles can be loaded into a `Theme` object using the `Theme.read` method, allowing for separation of style definitions from Python code and easier management.
SOURCE: https://github.com/textualize/rich/blob/master/docs/source/style.rst#_snippet_13

LANGUAGE: INI
CODE:
```
[styles]
info = dim cyan
warning = magenta
danger = bold red
```

----------------------------------------

TITLE: Grouping Panels with rich.console.Group (Python)
DESCRIPTION: This snippet demonstrates how to combine multiple `Panel` renderables into a single `Group` object. This allows them to be treated as a single renderable, suitable for embedding within another `Panel`. It requires importing `print`, `Group`, and `Panel` from the `rich` library.
SOURCE: https://github.com/textualize/rich/blob/master/docs/source/group.rst#_snippet_0

LANGUAGE: python
CODE:
```
from rich import print
from rich.console import Group
from rich.panel import Panel

panel_group = Group(
    Panel("Hello", style="on blue"),
    Panel("World", style="on red"),
)
print(Panel(panel_group))
```

----------------------------------------

TITLE: Converting ANSI Formatted Text with rich.text.Text.from_ansi (Python)
DESCRIPTION: This snippet demonstrates converting a string containing ANSI escape codes into a `Text` object using the `from_ansi` class method. It takes an ANSI-formatted string, parses its styles, and then prints the `spans` attribute of the resulting `Text` object, which represents the applied styles.
SOURCE: https://github.com/textualize/rich/blob/master/docs/source/text.rst#_snippet_2

LANGUAGE: Python
CODE:
```
text = Text.from_ansi("\033[1;35mHello\033[0m, World!")
console.print(text.spans)
```

----------------------------------------

TITLE: Applying Uniform Padding with Rich Python
DESCRIPTION: This snippet demonstrates the basic usage of the `Padding` class from the Rich library. It initializes a `Padding` object with the text 'Hello' and a uniform padding of 1 character, resulting in a blank line above/below and a space on left/right edges, then prints the padded text to the console.
SOURCE: https://github.com/textualize/rich/blob/master/docs/source/padding.rst#_snippet_0

LANGUAGE: python
CODE:
```
from rich import print
from rich.padding import Padding
test = Padding("Hello", 1)
print(test)
```

----------------------------------------

TITLE: Automatic Angular Rich Repr Generation with @rich.repr.auto in Python
DESCRIPTION: This snippet demonstrates how to automatically generate an angular-style Rich representation for a class by passing `angular=True` to the `@rich.repr.auto` decorator. This provides a compact, bracketed repr without requiring manual `__rich_repr__` implementation, similar to the manual angular setting.
SOURCE: https://github.com/textualize/rich/blob/master/docs/source/pretty.rst#_snippet_15

LANGUAGE: Python
CODE:
```
@rich.repr.auto(angular=True)
class Bird:
    def __init__(self, name, eats=None, fly=True, extinct=False):
        self.name = name
        self.eats = list(eats) if eats else []
        self.fly = fly
        self.extinct = extinct
```

----------------------------------------

TITLE: Truncating Containers with Rich pprint (Python)
DESCRIPTION: This snippet demonstrates using the `max_length` argument with `rich.pretty.pprint` to limit the number of elements displayed in containers. If the container exceeds the specified length, Rich truncates the output and indicates the number of hidden elements with an ellipsis.
SOURCE: https://github.com/textualize/rich/blob/master/docs/source/pretty.rst#_snippet_3

LANGUAGE: Python
CODE:
```
pprint(locals(), max_length=2)
```

----------------------------------------

TITLE: Advanced Console Rendering with `__rich_console__` Method (Python)
DESCRIPTION: This example illustrates implementing the `__rich_console__` method for complex object rendering. This method accepts `Console` and `ConsoleOptions` objects and yields multiple renderable objects, such as formatted text and a `Table`. It allows for dynamic and multi-part output, like displaying a student's ID followed by a detailed attribute table, providing fine-grained control over the console presentation.
SOURCE: https://github.com/textualize/rich/blob/master/docs/source/protocol.rst#_snippet_1

LANGUAGE: Python
CODE:
```
from dataclasses import dataclass
from rich.console import Console, ConsoleOptions, RenderResult
from rich.table import Table

@dataclass
class Student:
    id: int
    name: str
    age: int
    def __rich_console__(self, console: Console, options: ConsoleOptions) -> RenderResult:
        yield f"[b]Student:[/b] #{self.id}"
        my_table = Table("Attribute", "Value")
        my_table.add_row("name", self.name)
        my_table.add_row("age", str(self.age))
        yield my_table
```

----------------------------------------

TITLE: Displaying Emojis with Rich Console Markup
DESCRIPTION: This Python snippet shows how to render emojis using Rich console markup. By enclosing an emoji code (e.g., `:warning:`) within colons, Rich automatically replaces it with the corresponding Unicode emoji character when printed, enhancing visual communication in the terminal.
SOURCE: https://github.com/textualize/rich/blob/master/docs/source/markup.rst#_snippet_9

LANGUAGE: Python
CODE:
```
>>> from rich import print
>>> print(":warning:")
```

----------------------------------------

TITLE: Limiting Traceback Frames for Recursive Errors with Rich
DESCRIPTION: This snippet illustrates how to handle and display tracebacks for recursive errors using `console.print_exception()`. The `max_frames` argument is used to limit the number of frames displayed, preventing excessively long outputs for deep recursion errors while still providing relevant context.
SOURCE: https://github.com/textualize/rich/blob/master/docs/source/traceback.rst#_snippet_6

LANGUAGE: Python
CODE:
```
from rich.console import Console


def foo(n):
    return bar(n)


def bar(n):
    return foo(n)


console = Console()

try:
    foo(1)
except Exception:
    console.print_exception(max_frames=20)
```

----------------------------------------

TITLE: Setting Minimum Size for Rich Layout - Python
DESCRIPTION: This snippet illustrates how to set a minimum size constraint for a flexible layout. It assigns 10 to the 'minimum_size' attribute of the 'lower' layout, preventing it from shrinking below 10 rows (or characters) even when space is limited.
SOURCE: https://github.com/textualize/rich/blob/master/docs/source/layout.rst#_snippet_8

LANGUAGE: Python
CODE:
```
layout["lower"].minimum_size = 10
```

----------------------------------------

TITLE: Applying a Custom Highlighter as a Callable in Python
DESCRIPTION: This example shows an alternative way to use a custom highlighter by instantiating it and calling it directly on the text before printing. This allows for more granular control over when and where the custom highlighting is applied, rather than setting it globally on the `Console` constructor.
SOURCE: https://github.com/textualize/rich/blob/master/docs/source/highlighting.rst#_snippet_1

LANGUAGE: Python
CODE:
```
console = Console(theme=theme)
highlight_emails = EmailHighlighter()
console.print(highlight_emails("Send funds to money@example.org"))
```

----------------------------------------

TITLE: Customizing Default Rich Styles with Themes in Python
DESCRIPTION: This example illustrates how to override Rich's default styles by defining a custom theme that includes an existing style name, such as 'repr.number'. It shows how to change the appearance of numbers in Rich's representation output, demonstrating the flexibility of themes for customizing built-in behaviors.
SOURCE: https://github.com/textualize/rich/blob/master/docs/source/style.rst#_snippet_11

LANGUAGE: Python
CODE:
```
from rich.console import Console
from rich.theme import Theme
console = Console(theme=Theme({"repr.number": "bold green blink"}))
console.print("The total is 128")
```

----------------------------------------

TITLE: Printing Above Live Display with Rich Console (Python)
DESCRIPTION: Shows how to print or log messages above the active live display using the `live.console.print()` method. This allows for displaying static information or progress updates without interfering with the live-updating renderable.
SOURCE: https://github.com/textualize/rich/blob/master/docs/source/live.rst#_snippet_2

LANGUAGE: Python
CODE:
```
import time

from rich.live import Live
from rich.table import Table

table = Table()
table.add_column("Row ID")
table.add_column("Description")
table.add_column("Level")

with Live(table, refresh_per_second=4) as live:  # update 4 times a second to feel fluid
    for row in range(12):
        live.console.print(f"Working on row #{row}")
        time.sleep(0.4)
        table.add_row(f"{row}", f"description {row}", "[red]ERROR")
```

----------------------------------------

TITLE: Defining Default Rich Progress Bar Columns in Python
DESCRIPTION: This code illustrates the default column configuration for a `rich.progress.Progress` bar. It explicitly shows the `TextColumn`, `BarColumn`, `TaskProgressColumn`, and `TimeRemainingColumn` used by default, providing a template for understanding or replicating the standard progress bar appearance.
SOURCE: https://github.com/textualize/rich/blob/master/docs/source/progress.rst#_snippet_5

LANGUAGE: Python
CODE:
```
progress = Progress(
    TextColumn("[progress.description]{task.description}"),
    BarColumn(),
    TaskProgressColumn(),
    TimeRemainingColumn(),
)
```

----------------------------------------

TITLE: Preventing Nested Rich Live Contexts (Python)
DESCRIPTION: This snippet illustrates an incorrect usage pattern where an attempt is made to nest a console.status context within a rich.live.Live context. Rich's Live display does not support nested live contexts, and this operation will raise a LiveError. It highlights a limitation where only one live display can be active at a time.
SOURCE: https://github.com/textualize/rich/blob/master/docs/source/live.rst#_snippet_4

LANGUAGE: Python
CODE:
```
with Live(table, console=console):
    with console.status("working"):  # Will not work
        do_work()
```

----------------------------------------

TITLE: Custom Email Highlighting with RegexHighlighter in Python
DESCRIPTION: This snippet demonstrates how to create a custom highlighter using `rich.highlighter.RegexHighlighter` to style text matching a regular expression. It defines an `EmailHighlighter` class that applies a 'bold magenta' style to email addresses by defining a regex pattern and associating it with a custom theme. The `base_style` prefixes the group name to form the final style key.
SOURCE: https://github.com/textualize/rich/blob/master/docs/source/highlighting.rst#_snippet_0

LANGUAGE: Python
CODE:
```
from rich.console import Console
from rich.highlighter import RegexHighlighter
from rich.theme import Theme

class EmailHighlighter(RegexHighlighter):
    """Apply style to anything that looks like an email."""

    base_style = "example."
    highlights = [r"(?P<email>[\w-]+@([\w-]+\.)+[\w-]+)"]


theme = Theme({"example.email": "bold magenta"})
console = Console(highlighter=EmailHighlighter(), theme=theme)
console.print("Send funds to money@example.org")
```

----------------------------------------

TITLE: Updating Alternate Screen with Renderables in Rich (Python)
DESCRIPTION: This advanced example shows how to dynamically update content on the alternate screen using `screen.update()`. It displays a countdown within a styled panel, centered on the screen, demonstrating how Rich can crop content to fit and create interactive full-screen interfaces.
SOURCE: https://github.com/textualize/rich/blob/master/docs/source/console.rst#_snippet_27

LANGUAGE: Python
CODE:
```
from time import sleep

from rich.console import Console
from rich.align import Align
from rich.text import Text
from rich.panel import Panel

console = Console()

with console.screen(style="bold white on red") as screen:
    for count in range(5, 0, -1):
        text = Align.center(
            Text.from_markup(f"[blink]Don't Panic![/blink]\n{count}", justify="center"),
            vertical="middle",
        )
        screen.update(Panel(text))
        sleep(1)
```

----------------------------------------

TITLE: Creating a Rich Panel with Title and Subtitle
DESCRIPTION: This snippet illustrates how to add a title and subtitle to a `rich.panel.Panel`. The `title` argument places text at the top of the panel, and the `subtitle` argument places text at the bottom, enhancing the panel's presentation.
SOURCE: https://github.com/textualize/rich/blob/master/docs/source/panel.rst#_snippet_2

LANGUAGE: Python
CODE:
```
from rich import print
from rich.panel import Panel
print(Panel("Hello, [red]World!", title="Welcome", subtitle="Thank you"))
```

----------------------------------------

TITLE: Showing a Rich Layout - Python
DESCRIPTION: This snippet shows how to make a previously hidden layout visible again. Setting the 'visible' attribute of the 'upper' layout to True restores its visibility, allowing it to occupy its designated space. The layout is then printed to reflect the change.
SOURCE: https://github.com/textualize/rich/blob/master/docs/source/layout.rst#_snippet_10

LANGUAGE: Python
CODE:
```
layout["upper"].visible = True
print(layout)
```

----------------------------------------

TITLE: Vertically Aligning Table Cell Content in Rich (Python)
DESCRIPTION: Shows how to vertically align content within a table cell using the `rich.align.Align` class when adding a row. This example sets the vertical alignment of the "Title" content to "middle".
SOURCE: https://github.com/textualize/rich/blob/master/docs/source/tables.rst#_snippet_5

LANGUAGE: Python
CODE:
```
table.add_row(Align("Title", vertical="middle"))
```

----------------------------------------

TITLE: Using Custom Console with Rich Live Display (Python)
DESCRIPTION: This snippet demonstrates how to integrate a custom Console object with rich.live.Live. It shows passing my_console to the Live constructor, allowing all live display output to be directed through the specified console instance. This is useful for managing output streams or applying custom console configurations.
SOURCE: https://github.com/textualize/rich/blob/master/docs/source/live.rst#_snippet_3

LANGUAGE: Python
CODE:
```
from my_project import my_console

with Live(console=my_console) as live:
    my_console.print("[bold blue]Starting work!")
    ...
```

----------------------------------------

TITLE: Truncating Strings with Rich pprint (Python)
DESCRIPTION: This example illustrates how to use the `max_string` argument with `rich.pretty.pprint` to truncate long strings. Strings exceeding the specified length will be cut short, and the number of hidden characters will be appended to the output.
SOURCE: https://github.com/textualize/rich/blob/master/docs/source/pretty.rst#_snippet_4

LANGUAGE: Python
CODE:
```
pprint("Where there is a Will, there is a Way", max_string=21)
```

----------------------------------------

TITLE: Demonstrating Overlapping Styles in Rich Markup
DESCRIPTION: This Python example showcases how Rich console markup tags can overlap rather than requiring strict nesting. It applies 'bold' and 'italic' styles, demonstrating that a style can be closed even if another style opened within it is still active, providing flexible text formatting.
SOURCE: https://github.com/textualize/rich/blob/master/docs/source/markup.rst#_snippet_4

LANGUAGE: Python
CODE:
```
print("[bold]Bold[italic] bold and italic [/bold]italic[/italic]")
```

----------------------------------------

TITLE: Using Alternate Screen Mode in Rich (Python)
DESCRIPTION: This snippet demonstrates the use of Rich's `console.screen()` context manager to enter and exit the terminal's alternate screen mode. It displays the `locals()` dictionary on the alternate screen for 5 seconds, providing a temporary full-screen view without disturbing the main terminal content.
SOURCE: https://github.com/textualize/rich/blob/master/docs/source/console.rst#_snippet_26

LANGUAGE: Python
CODE:
```
from time import sleep
from rich.console import Console

console = Console()
with console.screen():
    console.print(locals())
    sleep(5)
```

----------------------------------------

TITLE: Customizing Status Spinner with Rich (Python)
DESCRIPTION: This example demonstrates customizing the spinner animation for `console.status` using the `spinner` parameter. It sets the spinner to "monkey" while "Monkeying around..." is displayed, providing unique visual feedback during a task.
SOURCE: https://github.com/textualize/rich/blob/master/docs/source/console.rst#_snippet_12

LANGUAGE: Python
CODE:
```
with console.status("Monkeying around...", spinner="monkey"):
    do_work()
```

----------------------------------------

TITLE: Using Shorthand Closing Tag in Rich Markup
DESCRIPTION: This Python snippet demonstrates the shorthand closing tag `[/]` in Rich console markup. When used, it automatically closes the most recently opened style, in this case, `[bold red]`, allowing for concise style management without explicitly naming the style in the closing tag.
SOURCE: https://github.com/textualize/rich/blob/master/docs/source/markup.rst#_snippet_3

LANGUAGE: Python
CODE:
```
print("[bold red]Bold and red[/] not bold or red")
```

----------------------------------------

TITLE: Importing Rich Console Instance (Python)
DESCRIPTION: This snippet shows how to import an already initialized `Console` instance from a project-specific module (e.g., `my_project.console`). This allows other parts of the application to reuse the same console object for consistent output.
SOURCE: https://github.com/textualize/rich/blob/master/docs/source/console.rst#_snippet_1

LANGUAGE: python
CODE:
```
from my_project.console import console
```

----------------------------------------

TITLE: Applying Multiple Styles Without Closing Tag in Rich
DESCRIPTION: This Python example illustrates how multiple Rich console styles can be combined and applied to a string. When no closing tag is provided, the applied styles (`bold`, `italic`, `yellow`, `on red`, `blink`) will persist until the end of the string, which is useful for styling an entire line.
SOURCE: https://github.com/textualize/rich/blob/master/docs/source/markup.rst#_snippet_2

LANGUAGE: Python
CODE:
```
print("[bold italic yellow on red blink]This text is impossible to read")
```

----------------------------------------

TITLE: Printing Locals with Rich Console (Python)
DESCRIPTION: This snippet demonstrates using `console.out` to print the local variables. It's a basic example of Rich's output capabilities, useful for debugging or inspecting the current scope.
SOURCE: https://github.com/textualize/rich/blob/master/docs/source/console.rst#_snippet_8

LANGUAGE: Python
CODE:
```
console.out("Locals", locals())
```

----------------------------------------

TITLE: Adding Rich Traceback Install to sitecustomize.py
DESCRIPTION: This Python code snippet is intended to be added to the `sitecustomize.py` file. When Python starts, this code will automatically install Rich as the default traceback handler for the entire virtual environment, enabling enhanced tracebacks for all executed scripts.
SOURCE: https://github.com/textualize/rich/blob/master/docs/source/traceback.rst#_snippet_4

LANGUAGE: Python
CODE:
```
from rich.traceback import install
install(show_locals=True)
```

----------------------------------------

TITLE: Applying Foreground Color by Number in Rich Python
DESCRIPTION: Shows how to specify a foreground color using its 256-color palette number (e.g., color(5)) within a style string for console.print.
SOURCE: https://github.com/textualize/rich/blob/master/docs/source/style.rst#_snippet_1

LANGUAGE: Python
CODE:
```
console.print("Hello", style="color(5)")
```

----------------------------------------

TITLE: Creating sitecustomize.py for Automatic Traceback Handler
DESCRIPTION: This command creates the `sitecustomize.py` file within a Python virtual environment's `site-packages` directory. This file is automatically executed by Python on startup, making it suitable for installing the Rich traceback handler globally for the environment.
SOURCE: https://github.com/textualize/rich/blob/master/docs/source/traceback.rst#_snippet_3

LANGUAGE: Bash
CODE:
```
$ touch .venv/lib/python3.9/site-packages/sitecustomize.py
```

----------------------------------------

TITLE: Combining Rich Style Objects
DESCRIPTION: Demonstrates how to combine existing Style objects using addition, allowing for the modification or extension of a base style (e.g., adding an underline to a cyan style).
SOURCE: https://github.com/textualize/rich/blob/master/docs/source/style.rst#_snippet_8

LANGUAGE: Python
CODE:
```
from rich.console import Console
from rich.style import Style
console = Console()

base_style = Style.parse("cyan")
console.print("Hello, World", style = base_style + Style(underline=True))
```

----------------------------------------

TITLE: Styling and Controlling Expansion of Padding with Rich Python
DESCRIPTION: This snippet demonstrates applying a background style ('on blue') to the padding and its content, and preventing the padding from expanding to the full terminal width by setting `expand=False`. This allows for more controlled visual presentation of padded elements within the Rich console.
SOURCE: https://github.com/textualize/rich/blob/master/docs/source/padding.rst#_snippet_2

LANGUAGE: python
CODE:
```
from rich import print
from rich.padding import Padding
test = Padding("Hello", (2, 4), style="on blue", expand=False)
print(test)
```

----------------------------------------

TITLE: Exporting SVG with Custom Theme in Rich Python
DESCRIPTION: This example demonstrates how to export console output as an SVG file while applying a specific terminal theme. It imports the `MONOKAI` theme and passes it to the `save_svg` method, allowing customization of the exported SVG's appearance.
SOURCE: https://github.com/textualize/rich/blob/master/docs/source/console.rst#_snippet_19

LANGUAGE: Python
CODE:
```
from rich.console import Console
from rich.terminal_theme import MONOKAI

console = Console(record=True)
console.save_svg("example.svg", theme=MONOKAI)
```

----------------------------------------

TITLE: Syntax Highlighting a File via Rich CLI in Python
DESCRIPTION: This command-line snippet shows how to use the `rich.syntax` module directly from the terminal to syntax highlight a specified file. It executes the module as a script, passing the file path as an argument. This provides a quick way to highlight files without writing a Python script.
SOURCE: https://github.com/textualize/rich/blob/master/docs/source/syntax.rst#_snippet_3

LANGUAGE: bash
CODE:
```
python -m rich.syntax syntax.py
```

----------------------------------------

TITLE: Displaying Rich Layout Tree Structure - Python
DESCRIPTION: This example demonstrates how to visualize the hierarchical structure of a Rich layout. Accessing and printing the 'tree' attribute of the layout object provides a summary of its nested components, which is useful for debugging complex layouts.
SOURCE: https://github.com/textualize/rich/blob/master/docs/source/layout.rst#_snippet_11

LANGUAGE: Python
CODE:
```
print(layout.tree)
```

----------------------------------------

TITLE: Overriding Highlighter for Rich Logs in Python
DESCRIPTION: This snippet demonstrates how to disable the default highlighter for a specific log message by setting `highlighter=None` in the `extra` argument. This is useful when certain parts of the log message should not be highlighted.
SOURCE: https://github.com/textualize/rich/blob/master/docs/source/logging.rst#_snippet_2

LANGUAGE: Python
CODE:
```
log.error("123 will not be highlighted", extra={"highlighter": None})
```

----------------------------------------

TITLE: Negating Style Attributes in Rich Python
DESCRIPTION: Demonstrates how to negate a style attribute (e.g., not bold) within a styled string using Rich's inline markup, allowing specific parts of text to opt out of an inherited style.
SOURCE: https://github.com/textualize/rich/blob/master/docs/source/style.rst#_snippet_5

LANGUAGE: Python
CODE:
```
console.print("foo [not bold]bar[/not bold] baz", style="bold")
```

----------------------------------------

TITLE: Default Rich Object Representation Output
DESCRIPTION: This snippet shows the default output format when Rich prints a dictionary containing custom `Bird` objects. Rich automatically omits default arguments and formats the output for readability, even with nested structures or limited terminal space.
SOURCE: https://github.com/textualize/rich/blob/master/docs/source/pretty.rst#_snippet_9

LANGUAGE: Python
CODE:
```
{
    'gull': Bird(
        'gull',
        eats=['fish', 'chips', 'ice cream', 'sausage rolls']
    ),
    'penguin': Bird('penguin', eats=['fish'], fly=False),
    'dodo': Bird('dodo', eats=['fruit'], fly=False, extinct=True)
}
```

----------------------------------------

TITLE: Displaying Rich Syntax CLI Help in Python
DESCRIPTION: This command-line snippet demonstrates how to access the help documentation for the `rich.syntax` command-line utility. Running this command will display all available arguments and options for the `rich.syntax` module. This is useful for discovering its full capabilities.
SOURCE: https://github.com/textualize/rich/blob/master/docs/source/syntax.rst#_snippet_4

LANGUAGE: bash
CODE:
```
python -m rich.syntax -h
```

----------------------------------------

TITLE: Displaying Markdown File from Command Line with Rich
DESCRIPTION: This command-line example shows how to use the `rich.markdown` module directly from the terminal to display the contents of a Markdown file (e.g., `README.md`) with Rich's rendering capabilities.
SOURCE: https://github.com/textualize/rich/blob/master/docs/source/markdown.rst#_snippet_1

LANGUAGE: Bash
CODE:
```
python -m rich.markdown README.md
```

----------------------------------------

TITLE: Importing Rich Print for Jupyter Notebooks (Python)
DESCRIPTION: This Python import statement brings the `print` function from the `rich.jupyter` module into scope. It enables experimental Jupyter notebook support, allowing Rich's enhanced printing capabilities to be used within a Jupyter environment for richer output.
SOURCE: https://github.com/textualize/rich/blob/master/CHANGELOG.md#_snippet_4

LANGUAGE: python
CODE:
```
from rich.jupyter import print
```

----------------------------------------

TITLE: Defining a Custom Class with Standard Repr (Python)
DESCRIPTION: This snippet defines a `Bird` class with an `__init__` method and a standard `__repr__` method. It then creates instances of `Bird` and stores them in a dictionary, demonstrating how a typical Python object's representation appears without Rich's custom protocol, often leading to verbose or wrapped output.
SOURCE: https://github.com/textualize/rich/blob/master/docs/source/pretty.rst#_snippet_7

LANGUAGE: Python
CODE:
```
class Bird:
    def __init__(self, name, eats=None, fly=True, extinct=False):
        self.name = name
        self.eats = list(eats) if eats else []
        self.fly = fly
        self.extinct = extinct

    def __repr__(self):
        return f"Bird({self.name!r}, eats={self.eats!r}, fly={self.fly!r}, extinct={self.extinct!r})"

BIRDS = {
    "gull": Bird("gull", eats=["fish", "chips", "ice cream", "sausage rolls"]),
    "penguin": Bird("penguin", eats=["fish"], fly=False),
    "dodo": Bird("dodo", eats=["fruit"], fly=False, extinct=True)
}
print(BIRDS)
```

----------------------------------------

TITLE: Compact Rich Object Representation Output
DESCRIPTION: This snippet illustrates how Rich adapts its object representation for better readability when terminal space is limited or objects are deeply nested. It demonstrates Rich's ability to reformat the output to fit constraints while maintaining clarity.
SOURCE: https://github.com/textualize/rich/blob/master/docs/source/pretty.rst#_snippet_10

LANGUAGE: Python
CODE:
```
{
    'gull': Bird(
        'gull',
        eats=[
            'fish',
            'chips',
            'ice cream',
            'sausage rolls'
        ]
    ),
    'penguin': Bird(
        'penguin',
        eats=['fish'],
        fly=False
    ),
    'dodo': Bird(
        'dodo',
        eats=['fruit'],
        fly=False,
        extinct=True
    )
}
```

----------------------------------------

TITLE: Listing Available Rich Spinners via Command Line
DESCRIPTION: This shell command executes the rich.spinner module directly to display all available spinner animations that can be used with the rich.console.Console.status method. It helps users preview and select a suitable spinner by specifying the spinner parameter.
SOURCE: https://github.com/textualize/rich/blob/master/README.md#_snippet_14

LANGUAGE: shell
CODE:
```
python -m rich.spinner
```

----------------------------------------

TITLE: Viewing Default Rich Themes and Styles via CLI
DESCRIPTION: These commands show how to inspect the default styles and theme built into Rich directly from the command line. Running `python -m rich.theme` displays the current active theme, while `python -m rich.default_styles` lists all default styles, which is useful for understanding and customizing Rich's appearance.
SOURCE: https://github.com/textualize/rich/blob/master/docs/source/style.rst#_snippet_12

LANGUAGE: Shell
CODE:
```
python -m rich.theme
python -m rich.default_styles
```

----------------------------------------

TITLE: Specifying Emoji Variants in Rich Markup
DESCRIPTION: This Python snippet demonstrates how to explicitly choose between emoji variants (full-color 'emoji' or monochrome 'text') using Rich console markup. By appending `-emoji` or `-text` to the emoji code, users can control the visual representation of emojis like `:red_heart:` in their terminal output.
SOURCE: https://github.com/textualize/rich/blob/master/docs/source/markup.rst#_snippet_10

LANGUAGE: Python
CODE:
```
>>> from rich import print
>>> print(":red_heart-emoji:")
>>> print(":red_heart-text:")
```

----------------------------------------

TITLE: Low-Level Console Rendering with `__rich_console__` and Segments (Python)
DESCRIPTION: This snippet demonstrates using the `__rich_console__` method to yield `Segment` objects for granular control over rendering. Each `Segment` combines text with a specific `Style`, allowing for multi-colored or highly customized output. This approach provides the lowest level of control, enabling precise styling of individual text parts within the console output.
SOURCE: https://github.com/textualize/rich/blob/master/docs/source/protocol.rst#_snippet_2

LANGUAGE: Python
CODE:
```
class MyObject:
    def __rich_console__(self, console: Console, options: ConsoleOptions) -> RenderResult:
        yield Segment("My", Style(color="magenta"))
        yield Segment("Object", Style(color="green"))
        yield Segment("()", Style(color="cyan"))
```

----------------------------------------

TITLE: Running Rich Test Card via CLI (Python)
DESCRIPTION: This command executes the main `rich` module from the command line, specifically to run a 'test card'. This utility is used to display a comprehensive set of Rich's features and styling capabilities, useful for testing terminal compatibility and visual fidelity.
SOURCE: https://github.com/textualize/rich/blob/master/CHANGELOG.md#_snippet_3

LANGUAGE: shell
CODE:
```
python -m rich
```

----------------------------------------

TITLE: Viewing Rich Markdown Command Line Arguments
DESCRIPTION: This command-line snippet demonstrates how to access the help documentation for the `rich.markdown` module, displaying all available arguments and options for its command-line usage.
SOURCE: https://github.com/textualize/rich/blob/master/docs/source/markdown.rst#_snippet_2

LANGUAGE: Bash
CODE:
```
python -m rich.markdown -h
```

----------------------------------------

TITLE: Measuring Renderable Width with `__rich_measure__` Method (Python)
DESCRIPTION: This example shows how to implement the `__rich_measure__` method, which is crucial for Rich to determine the optimal width for rendering custom objects. This method takes `Console` and `ConsoleOptions` and returns a `Measurement` object, specifying the minimum and maximum character width required. For a `ChessBoard`, it defines a minimum width of 8 characters and allows the maximum width to be the available console width.
SOURCE: https://github.com/textualize/rich/blob/master/docs/source/protocol.rst#_snippet_3

LANGUAGE: Python
CODE:
```
class ChessBoard:
    def __rich_measure__(self, console: Console, options: ConsoleOptions) -> Measurement:
        return Measurement(8, options.max_width)
```

----------------------------------------

TITLE: Angular Bracket Style Rich Object Representation Output
DESCRIPTION: This snippet shows the output format when Rich prints a dictionary of `Bird` objects after the `__rich_repr__` method has been configured to use the angular bracket style. This compact format is suitable for objects where the constructor arguments are not directly represented in the repr.
SOURCE: https://github.com/textualize/rich/blob/master/docs/source/pretty.rst#_snippet_12

LANGUAGE: Python
CODE:
```
{
    'gull': <Bird 'gull' eats=['fish', 'chips', 'ice cream', 'sausage rolls']>,
    'penguin': <Bird 'penguin' eats=['fish'] fly=False>,
    'dodo': <Bird 'dodo' eats=['fruit'] fly=False extinct=True>
}
```

----------------------------------------

TITLE: Running Rich Layout Example via Command Line
DESCRIPTION: This command line snippet demonstrates how to run the built-in example for the `rich.layout` module. It serves as a quick way to visualize the capabilities of the `Layout` class without writing any code.
SOURCE: https://github.com/textualize/rich/blob/master/docs/source/layout.rst#_snippet_0

LANGUAGE: bash
CODE:
```
python -m rich.layout
```

----------------------------------------

TITLE: Running Rich Status Demo (Shell)
DESCRIPTION: This command line snippet executes the `rich.status` module as a script to demonstrate its features, including the spinner animation. It's a quick way to see the `status` functionality in action without writing a full Python script.
SOURCE: https://github.com/textualize/rich/blob/master/docs/source/console.rst#_snippet_10

LANGUAGE: Shell
CODE:
```
python -m rich.status
```

----------------------------------------

TITLE: Running Rich Tree Demonstration
DESCRIPTION: This command executes the built-in demonstration of the Rich Tree class directly from the Python module. It showcases the capabilities of the Tree view in the terminal.
SOURCE: https://github.com/textualize/rich/blob/master/docs/source/tree.rst#_snippet_0

LANGUAGE: Bash
CODE:
```
python -m rich.tree
```

----------------------------------------

TITLE: Demonstrating Rich Tree Rendering via Command Line
DESCRIPTION: This shell command runs a built-in demonstration of Rich's tree rendering capabilities. It's useful for quickly seeing how hierarchical data can be visually represented with guide lines, similar to a file structure or other nested information.
SOURCE: https://github.com/textualize/rich/blob/master/README.md#_snippet_15

LANGUAGE: shell
CODE:
```
python -m rich.tree
```

----------------------------------------

TITLE: Enabling Angular Bracket Style Rich Repr in Python
DESCRIPTION: This snippet demonstrates how to enable the "angular bracket" style of representation for a class's Rich repr. By setting the `angular` attribute of the `__rich_repr__` method to `True`, Rich will format the object's representation using angle brackets, typically used when direct constructor recreation is not straightforward.
SOURCE: https://github.com/textualize/rich/blob/master/docs/source/pretty.rst#_snippet_11

LANGUAGE: Python
CODE:
```
__rich_repr__.angular = True
```

----------------------------------------

TITLE: Implementing a Custom Highlighter with Base Highlighter Class in Python
DESCRIPTION: This snippet illustrates how to create a custom highlighter by extending the base `rich.highlighter.Highlighter` class. It overrides the `highlight` method to apply a unique, random color to each character in the input text, demonstrating fine-grained control over text styling beyond regular expression matching.
SOURCE: https://github.com/textualize/rich/blob/master/docs/source/highlighting.rst#_snippet_2

LANGUAGE: Python
CODE:
```
from random import randint

from rich import print
from rich.highlighter import Highlighter


class RainbowHighlighter(Highlighter):
    def highlight(self, text):
        for index in range(len(text)):
            text.stylize(f"color({randint(16, 255)})", index, index + 1)


rainbow = RainbowHighlighter()
print(rainbow("I must not fear. Fear is the mind-killer."))
```

----------------------------------------

TITLE: Running Rich Repr Protocol Example (Shell)
DESCRIPTION: This command executes the `rich.repr` module from the command line, providing a demonstration of how the Rich repr protocol formats custom objects. It's used to visualize the enhanced representation capabilities for user-defined classes.
SOURCE: https://github.com/textualize/rich/blob/master/docs/source/pretty.rst#_snippet_6

LANGUAGE: Shell
CODE:
```
python -m rich.repr
```

----------------------------------------

TITLE: Running Rich Markup Examples via CLI
DESCRIPTION: This command line instruction executes the `rich.markup` module, which demonstrates various examples of Rich console markup syntax and its capabilities directly in the terminal. It's used for quick visual inspection of markup features.
SOURCE: https://github.com/textualize/rich/blob/master/docs/source/markup.rst#_snippet_0

LANGUAGE: Bash
CODE:
```
python -m rich.markup
```

----------------------------------------

TITLE: Listing Available Rich Spinners (Shell)
DESCRIPTION: This command line snippet runs the `rich.spinner` module to display a comprehensive list of all available spinner choices. These spinners can be used with the `spinner` parameter in `console.status` to customize the animation.
SOURCE: https://github.com/textualize/rich/blob/master/docs/source/console.rst#_snippet_13

LANGUAGE: Shell
CODE:
```
python -m rich.spinner
```

----------------------------------------

TITLE: Listing Available Emojis via Rich CLI
DESCRIPTION: This command line instruction executes the `rich.emoji` module, which displays a comprehensive list of all supported emoji codes and their corresponding Unicode characters available for use with Rich console markup. It's a utility for discovering and referencing emoji options.
SOURCE: https://github.com/textualize/rich/blob/master/docs/source/markup.rst#_snippet_11

LANGUAGE: Bash
CODE:
```
python -m rich.emoji
```

----------------------------------------

TITLE: Checking Code Formatting with Make
DESCRIPTION: This command uses `make` to check if the project's code adheres to the `black` formatting standards. It performs a dry run without modifying files, reporting any formatting inconsistencies.
SOURCE: https://github.com/textualize/rich/blob/master/CONTRIBUTING.md#_snippet_6

LANGUAGE: Shell
CODE:
```
make format-check
```

----------------------------------------

TITLE: Running Tests with Make
DESCRIPTION: This command executes the project's test suite using `make`. It's a convenient shortcut for running all defined tests and typically includes a coverage report, helping identify untested code.
SOURCE: https://github.com/textualize/rich/blob/master/CONTRIBUTING.md#_snippet_2

LANGUAGE: Shell
CODE:
```
make test
```

----------------------------------------

TITLE: Testing Rich Terminal Output
DESCRIPTION: This command runs a built-in test or demonstration of Rich's capabilities directly in your terminal, allowing you to verify its functionality and see examples of its output.
SOURCE: https://github.com/textualize/rich/blob/master/README.md#_snippet_1

LANGUAGE: shell
CODE:
```
python -m rich
```

----------------------------------------

TITLE: Running Rich Syntax Module via CLI (Python)
DESCRIPTION: This command executes the `rich.syntax` module from the command line. It's designed for highlighting code syntax in the terminal, providing a quick way to view syntax-highlighted files or code snippets without a full application.
SOURCE: https://github.com/textualize/rich/blob/master/CHANGELOG.md#_snippet_1

LANGUAGE: shell
CODE:
```
python -m rich.syntax
```

----------------------------------------

TITLE: Running Rich Pretty Print Module (Shell)
DESCRIPTION: This command executes the `rich.pretty` module directly from the command line, demonstrating its default pretty printing capabilities for various Python data structures. It shows how Rich automatically adjusts output to fit the terminal width.
SOURCE: https://github.com/textualize/rich/blob/master/docs/source/pretty.rst#_snippet_0

LANGUAGE: Shell
CODE:
```
python -m rich.pretty
```

----------------------------------------

TITLE: Running Rich Prompt Examples from Command Line (Shell)
DESCRIPTION: Provides the command-line instruction to execute the built-in examples of `rich.prompt` classes. This allows users to interactively experience the various prompt functionalities directly from their terminal.
SOURCE: https://github.com/textualize/rich/blob/master/docs/source/prompt.rst#_snippet_5

LANGUAGE: Shell
CODE:
```
python -m rich.prompt
```

----------------------------------------

TITLE: Running Rich Progress Demo from Command Line
DESCRIPTION: This command demonstrates the Rich progress display feature directly from the command line. It runs a built-in example to show how the progress bars and task information are rendered.
SOURCE: https://github.com/textualize/rich/blob/master/docs/source/progress.rst#_snippet_0

LANGUAGE: Python
CODE:
```
python -m rich.progress
```

----------------------------------------

TITLE: Running Rich Theme Module via CLI (Python)
DESCRIPTION: This command executes the `rich.theme` module from the command line. It's likely used for managing or inspecting Rich themes, allowing users to preview or configure terminal styling options directly.
SOURCE: https://github.com/textualize/rich/blob/master/CHANGELOG.md#_snippet_2

LANGUAGE: shell
CODE:
```
python -m rich.theme
```

----------------------------------------

TITLE: Running Rich Traceback Example via CLI
DESCRIPTION: This command line instruction demonstrates how to execute the `rich.traceback` module directly from the Python interpreter to see an example of a Rich-formatted traceback. It's a quick way to preview the enhanced traceback rendering.
SOURCE: https://github.com/textualize/rich/blob/master/docs/source/traceback.rst#_snippet_0

LANGUAGE: Bash
CODE:
```
python -m rich.traceback
```

----------------------------------------

TITLE: Running Rich Markdown Module via CLI (Python)
DESCRIPTION: This command executes the `rich.markdown` module directly from the command line. It's used to render Markdown content in the terminal, potentially with options for justification and code themes. This is a utility for quick Markdown rendering without writing a Python script.
SOURCE: https://github.com/textualize/rich/blob/master/CHANGELOG.md#_snippet_0

LANGUAGE: shell
CODE:
```
python -m rich.markdown
```

----------------------------------------

TITLE: Generating Rich Box Styles Demo
DESCRIPTION: This command-line snippet executes the `rich.box` module directly, which typically generates and displays a table showcasing all available box drawing characters and styles. It's used for demonstration and testing purposes.
SOURCE: https://github.com/textualize/rich/blob/master/docs/source/appendix/box.rst#_snippet_1

LANGUAGE: Shell
CODE:
```
python -m rich.box
```

----------------------------------------

TITLE: Copying Generated HTML to Rich Benchmarks Repo (Shell)
DESCRIPTION: This command copies the locally generated benchmark HTML files from the `rich` repository's `benchmarks/html` directory into the root of the `rich-benchmarks` repository. This step is crucial for updating the public benchmark dashboard.
SOURCE: https://github.com/textualize/rich/blob/master/benchmarks/README.md#_snippet_6

LANGUAGE: Shell
CODE:
```
cp -r ../rich/benchmarks/html/* .
```

----------------------------------------

TITLE: Setting Up Virtual Environment with Poetry
DESCRIPTION: This command creates and enters an isolated virtual environment for the Rich project using Poetry. If an environment already exists, it simply activates it, ensuring project dependencies are managed separately from the system's Python installation.
SOURCE: https://github.com/textualize/rich/blob/master/CONTRIBUTING.md#_snippet_0

LANGUAGE: Shell
CODE:
```
poetry shell
```

----------------------------------------

TITLE: Performing Type Checking with Make
DESCRIPTION: This command initiates type checking for the Rich project using `make`. It leverages `mypy` to analyze the codebase for type consistency, ensuring that all new and existing code adheres to type annotations.
SOURCE: https://github.com/textualize/rich/blob/master/CONTRIBUTING.md#_snippet_4

LANGUAGE: Shell
CODE:
```
make typecheck
```

----------------------------------------

TITLE: Building Documentation with Make
DESCRIPTION: This command builds the static HTML documentation for the project using `make`. It processes the source files and generates the output in the `docs/build/html` directory, making the documentation accessible for review.
SOURCE: https://github.com/textualize/rich/blob/master/CONTRIBUTING.md#_snippet_9

LANGUAGE: Shell
CODE:
```
make docs
```

----------------------------------------

TITLE: Running Tests with Pytest Directly
DESCRIPTION: This command runs the project's test suite directly using `pytest`, providing a detailed coverage report. It's an alternative to `make test` for environments where `make` is not available or preferred, ensuring all tests pass and highlighting missing coverage.
SOURCE: https://github.com/textualize/rich/blob/master/CONTRIBUTING.md#_snippet_3

LANGUAGE: Shell
CODE:
```
pytest --cov-report term-missing --cov=rich tests/ -vv
```

----------------------------------------

TITLE: Running Benchmarks Against Latest Commit (Shell)
DESCRIPTION: This command runs the benchmarks against the most recent commit on the currently checked-out branch. It is useful for quickly testing performance changes introduced by recent development.
SOURCE: https://github.com/textualize/rich/blob/master/benchmarks/README.md#_snippet_2

LANGUAGE: Shell
CODE:
```
asv run HEAD^!
```

----------------------------------------

TITLE: Previewing Local Benchmark Dashboard (Shell)
DESCRIPTION: This command launches a local web server to preview the generated benchmark dashboard HTML. It allows developers to verify the appearance and functionality of the dashboard before publishing it.
SOURCE: https://github.com/textualize/rich/blob/master/benchmarks/README.md#_snippet_5

LANGUAGE: Shell
CODE:
```
asv preview
```

----------------------------------------

TITLE: Running Benchmarks for Specified Tags (Shell)
DESCRIPTION: This command executes benchmarks for specific tags or commits listed in the `asvhashfile`. It is used to benchmark historical versions or specific releases, ensuring consistent performance tracking across different project milestones.
SOURCE: https://github.com/textualize/rich/blob/master/benchmarks/README.md#_snippet_4

LANGUAGE: Shell
CODE:
```
asv run HASHFILE:asvhashfile
```

----------------------------------------

TITLE: Running Benchmarks Against Master Branch (Shell)
DESCRIPTION: This command executes the configured benchmarks against the `master` branch of the Rich repository. It is used to establish a baseline performance measurement for the main development line.
SOURCE: https://github.com/textualize/rich/blob/master/benchmarks/README.md#_snippet_1

LANGUAGE: Shell
CODE:
```
asv run
```

----------------------------------------

TITLE: Displaying Airspeed Velocity Help (Shell)
DESCRIPTION: This command displays the full list of available options and commands for the Airspeed Velocity (asv) benchmarking tool. It is recommended for understanding all possible configurations and actions.
SOURCE: https://github.com/textualize/rich/blob/master/benchmarks/README.md#_snippet_0

LANGUAGE: Shell
CODE:
```
asv run --help
```

----------------------------------------

TITLE: Generating Static Benchmark Website (Shell)
DESCRIPTION: This command generates a static HTML website from the benchmark results, which can then be used for browsing and visualizing the performance data. The output HTML files are typically found in `benchmarks/html`.
SOURCE: https://github.com/textualize/rich/blob/master/benchmarks/README.md#_snippet_3

LANGUAGE: Shell
CODE:
```
asv publish
```

----------------------------------------

TITLE: Installing Documentation Dependencies
DESCRIPTION: This command installs the necessary Python packages required to build the project's documentation. It reads dependencies from `requirements.txt` located in the `docs` directory, preparing the environment for documentation generation.
SOURCE: https://github.com/textualize/rich/blob/master/CONTRIBUTING.md#_snippet_8

LANGUAGE: Shell
CODE:
```
pip install -r requirements.txt
```

----------------------------------------

TITLE: Installing Project Dependencies with Poetry
DESCRIPTION: This command installs all required project dependencies into the currently active Poetry virtual environment. It reads the project's `pyproject.toml` file to determine and install the necessary packages, preparing the environment for development.
SOURCE: https://github.com/textualize/rich/blob/master/CONTRIBUTING.md#_snippet_1

LANGUAGE: Shell
CODE:
```
poetry install
```

----------------------------------------

TITLE: Formatting Code with Make
DESCRIPTION: This command uses `make` to automatically format the project's code using `black`. It modifies files in place to ensure they conform to the defined formatting standards, improving code readability and consistency.
SOURCE: https://github.com/textualize/rich/blob/master/CONTRIBUTING.md#_snippet_7

LANGUAGE: Shell
CODE:
```
make format
```

----------------------------------------

TITLE: Performing Type Checking with Mypy Directly
DESCRIPTION: This command performs type checking on the Rich project directly using `mypy`. It's an alternative to `make typecheck` for environments without `make`, ensuring type annotations are correctly applied and no type errors are present.
SOURCE: https://github.com/textualize/rich/blob/master/CONTRIBUTING.md#_snippet_5

LANGUAGE: Shell
CODE:
```
mypy -p rich --config-file= --ignore-missing-imports --no-implicit-optional --warn-unreachable
```
