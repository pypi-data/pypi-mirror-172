# Loading Display

Simple loading bar and spinner for the terminal.

## spinner

Prints unicode frames for a spinning animation.

Usage:

```py
from loading_display import spinner

s = spinner()
while loading:
    next(s)
```

## Loading bar

Prints a progress bar.

```py
from loading_display import loading_bar

while loading:
    loading_bar(current_progress, total=total_size, bar_length=10, show_percentage=True)
```
