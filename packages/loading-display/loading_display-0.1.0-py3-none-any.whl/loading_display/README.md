# Loading Display

[![Downloads](https://static.pepy.tech/personalized-badge/loading-display?period=total&units=international_system&left_color=black&right_color=blue&left_text=Downloads)](https://pepy.tech/project/loading-display)

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

The icons used as frames in the spinner can be changed using the `icons` parameter:

```py
>>> from loading_display import spinner
>>> s = spinner(icons=['🌑', '🌒', '🌓', '🌔', '🌕', '🌖', '🌗', '🌘'])
>>> while 1:
...     next(s)
```

## Loading bar

Prints a progress bar.

Usage:

```py
from loading_display import loading_bar

while loading:
    loading_bar(current_progress, 
                total=total_size, 
                bar_length=10, 
                show_percentage=True)
```

Default appearance:

```txt
████████████████████ 100.0 %
```

The appearance can be customized with the `icon` parameter.
