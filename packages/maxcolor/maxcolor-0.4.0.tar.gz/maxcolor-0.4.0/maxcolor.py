# max_logger/color.py
import re
from random import choice
from typing import List

from rich.color import Color
from rich.console import Console
from rich.panel import Panel
from rich.progress import (
    BarColumn,
    MofNCompleteColumn,
    Progress,
    SpinnerColumn,
    TextColumn,
    TimeElapsedColumn,
    TimeRemainingColumn,
)
from rich.table import Column
from rich.text import Text
from rich.theme import Theme
from rich.traceback import install

__version__ = "0.4.0"

theme = Theme(
    {
        "debug": "bold bright_cyan",
        "cyan": "#00ffff",
        "info": "bold cornflower_blue",
        "cornflower_blue": "#249df1",
        "blue": "bold #0000FF",
        "success": "bold bright_green",
        "green": "#00ff00",
        "warning": "bold bright_yellow",
        "yellow": "#ffff00",
        "error": "bold orange1",
        "orange": "#ff8800",
        "critical": "bold reverse #F00000",
        "red": "#ff0000",
        "key": "italic blue_violet",
        "blue_violet": "#5f00ff",
        "value": "bold bright_white",
        "white": "#ffffff",
        "title": "bold purple",
        "purple": "#af00ff",
        "bold": "bold",
        "italic": "italic",
        "reverse": "reverse",
    }
)

# . Console & Traceback
console = Console(theme=theme)
install(console=console)

# . Progress
text_column = TextColumn("[progress.description]{task.description}")
spinner_column = SpinnerColumn()
bar_column = BarColumn(
    bar_width=None, finished_style="green", table_column=Column(ratio=3)
)
mofn_column = MofNCompleteColumn()
time_elapsed_column = TimeElapsedColumn()
time_remaining_column = TimeRemainingColumn()
progress = Progress(
    text_column,
    spinner_column,
    bar_column,
    mofn_column,
    time_elapsed_column,
    time_remaining_column,
    console=console,
    refresh_per_second=10,
    auto_refresh=True,
)

# , Helper Function 1
def hashtag(color: str) -> str:
    """Add a `#` to the color if it is missing."""
    hex_regex = re.compile(r"^#(?:[0-9a-fA-F]{3}){1,2}$")
    if hex_regex.match(color):
        return color
    elif "#" not in color:
        color = f"#{color}"
        return color
    else:
        raise ValueError(f"Invalid Hex Color: {color}")


# , Helper Function 2
def validate_colors(color1: str, color2: str) -> List[str]:
    """Validate the colors."""
    color1 = hashtag(color1)
    color2 = hashtag(color2)
    return [color1, color2]


# . Gradient Function 1
def rainbow(message: str, num_of_gradients: int = 4) -> Text:
    """Rainbow text."""
    red = "#ff0000"
    orange = "#ff7f00"
    yellow = "#ffff00"
    green = "#00ff00"
    blue = "#61bdff"
    violet = "#7f00ff"
    magenta = "#ff00ff"
    colors1 = [red, orange, yellow, green, blue, violet, magenta]
    colors2 = [orange, yellow, green, blue, violet, magenta, red]
    colors3 = [yellow, green, blue, violet, magenta, red, orange]
    colors4 = [green, blue, violet, magenta, red, orange, yellow]
    colors5 = [blue, violet, magenta, red, orange, yellow, green]
    colors6 = [violet, magenta, red, orange, yellow, green, blue]
    colors7 = [magenta, red, orange, yellow, green, blue, violet]
    colors = [colors1, colors2, colors3, colors4, colors5, colors6, colors7]

    rainbow = choice(colors)
    text = Text(message)
    size = len(text)

    if num_of_gradients > 7:
        num_of_gradients = 7
    gradient_size = size // (num_of_gradients - 1)
    gradient_text = Text()

    for index in range(0, num_of_gradients):
        begin = index * gradient_size
        end = (index + 1) * gradient_size
        sub_text = text[begin:end]

        if index < num_of_gradients:
            color1 = Color.parse(rainbow[index])
            color1_triplet = color1.triplet
            r1 = color1_triplet[0]  # type: ignore
            g1 = color1_triplet[1]  # type: ignore
            b1 = color1_triplet[2]  # type: ignore
            color2 = Color.parse(rainbow[index + 1])
            color2_triplet = color2.triplet
            r2 = color2_triplet[0]  # type: ignore
            g2 = color2_triplet[1]  # type: ignore
            b2 = color2_triplet[2]  # type: ignore
            dr = r2 - r1
            dg = g2 - g1
            db = b2 - b1

        for index in range(gradient_size):
            blend = index / gradient_size
            color = f"#{int(r1 + dr * blend):02X}{int(g1 + dg * blend):02X}{int(b1 + db * blend):02X}"  # type: ignore
            sub_text.stylize(color, index, index + 1)
        gradient_text = Text.assemble(gradient_text, sub_text)

    return gradient_text


# . Gradient Function 2 (Panel)
def gradient_panel(text: str, title: str | None = None, colors: int = 4) -> Panel:
    """Gradient panel."""
    if colors <= 7:
        gradient_text = rainbow(text, colors)

    else:
        raise ValueError(
            f"Invalid number: {colors}. Colors must be an integer between 1 and 7."
        )
    split_lines = text.splitlines()
    pad = False
    if len(split_lines) > 1:
        pad = True

    if title:
        if pad:
            return Panel(
                gradient_text,
                title=f"[bold bright_white]{title}[/bold bright_white]",
                title_align="left",
                border_style="bright_white",
                expand=False,
                style="bold",
                padding=(1, 4),
            )
        else:
            return Panel(
                gradient_text,
                title=f"[bold bright_white]{title}[/bold bright_white]",
                title_align="left",
                border_style="bright_white",
                expand=False,
                style="bold",
                padding=(1, 4),
            )
    else:
        if pad:
            return Panel(
                gradient_text,
                border_style="bright_white",
                expand=False,
                style="bold",
                padding=(1, 4),
            )
        else:
            return Panel(
                gradient_text, border_style="bright_white", expand=False, style="bold", padding=(1, 4)
            )
