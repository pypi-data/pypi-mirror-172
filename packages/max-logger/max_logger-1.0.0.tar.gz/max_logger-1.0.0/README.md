---
title: max_logger README
author: Max Ludden
email: dev@maxludden.com
edited: 10-20-2022
CSS: style.css
---

# `max_logger`
The main purpose of the module is to automate my custom logging. It's based on the most excellent [loguru](https://github.com/Delgan/loguru) module and automatically sets up the loguru sinks that I find most useful. In addition it also provides a number of helper functions for working with Rich Python by [Textualize](https://www.textualize.io/), including the ability to print gradient text and panels.

## Instillation

<br />
<br />

### Install using `pipx`
```bash
pipx install max_logger
```

<br />
<br />

### Install using `pip`
```bash
pip install max_logger
```
<br />
<br />

### Install using `poetry`
```bash
poetry add max_logger
```
<br />

It's as simple as that. This module is available on PyPi and can be installed using your favorite python package manager (`pipx`, `pip`, `poetry`).

<br />
<br />
<br />

# Usage
```Python
from max_logger import log

>>> log.info("Hello, World!)
```
It's as simple as that. It is useful to note that you may import a custom formatted Rich Console & Progress from the modules as well. This is useful if you want to use the same console for your own logging.



```Python
from time import sleep
from max_logger import console, progress

with progress:
    task1 = progress.add_task("task1", total=10)
    for i in range(1,11):
        progress.update(task1, advance=1)
        sleep(0.1)
        smiles = ":smile:" * i
        console.print(f"[bright_red]♥︎[/] [bold purple1]I really like Max's Logger![/][#00ff00] ☘︎[/]")
```



<figure>
    <img src=https://i.imgur.com/IdKDdzE.png alt="Example of Rich Console" />
    <figcaption>Example of Rich Console</figcaption>
</figure>



<br />
<br />
<br />

# Gradient Text
There are also a number of helper function to allow the printing of gradient text.

## `rainbow`
```Python
def rainbow(message: str, num_of_gradients: int = 4) -> Text:
    """Prints a rainbow gradient of the message.

    Args:
        message (str): The message to print.
        num_of_gradients (int, optional): The number of gradients to use. Defaults to 4. Must be between 1 and 6.

    Returns:
        Text: The message as a Gradient Rich Text object.
    """
```

```Python
from max_logger import rainbow

console.print(rainbow("I think this is a lot more fun. 🌈"))
```
<br />
<figure>
    <img src="https://i.imgur.com/4PDNxIA.png" alt="Example of rainbow text" />
    <figcaption>Example of rainbow text</figcaption>
</figure>

<br />
<br />

## Gradient Panel
This automates the creation of a panel with gradient text and an optional title.


```Python
def gradient_panel(text: str, title: str | None = None, num_of_gradients: int = 4) -> Panel:
    """
        Args:
            text (str): The content of the panel.
            title (Optional[str]): The title of the panel.
            num_of_gradients (Optional[int]): The number of gradients to use. Valid arguments are between 1 - 6.

        Returns:
            panel (Panel): A gradient panel.
    """

console.print(gradient_panel("This is even better!!!, title="Gradient Panel"))
```

<figure>
    <img src="https://i.imgur.com/5H2qksr.png" alt="Gradient Panel" />
    <figcaption>Gradient Panel Example</figcaption>
</figure>

<br />
<br />

## `gradient`


```Python
def gradient(message: str, start_color: str, end_color: str) -> Text:
    """Prints a gradient of the message.

    Args:
        message (str): The message to print.
        start_color (str): The HEX start color of the gradient.
        end_color (str): The HEX end color of the gradient.

    Returns:
        Text: The message as a Gradient Rich Text object.
    """
```

##### Example `gradient` usage:
```Python
from max_logger import gradient

console.print("gradient[^gradient]Simple is always nice...[/]", "#FF0000", "#FF8800"), justify="center")
```


<figure>
    <img src="https://i.imgur.com/CBZ79sC.png" alt="Two Color Gradient" />
    <figcaption>Gradient Panel Example</figcaption>
</figure>
