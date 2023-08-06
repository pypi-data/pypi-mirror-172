import time
import math


def bar(current_progress: int,
        total=100,
        bar_length=10,
        show_percentage=False,
        icon='\u2588'):
    '''
    Prints out a loading bar with the given loading progression
    based on `current_progress` and `total`. The with of the loading bar 
    in characters is based on `bar_length`.
    If `show_percentage` is `True`, the percentage with be added 
    at the end of the loading bar.
    '''
    percentage = current_progress / (total / 100)
    q = math.floor(percentage / (100 / bar_length))
    remaining = bar_length - q
    bar = f'{icon * min(q, bar_length)}{" "*remaining}'
    if show_percentage:
        print(f'\r{bar} {round(percentage, 1)} %', end='')
    else:
        print(f'\r{bar}', end='')


def spinner(icons=["\u25DC ", " \u25DD", " \u25DE", "\u25DF "]):
    '''
    Returns a spinner Generator. 
    Pass the instance of this to next() to print the next frame of the spinner.
    '''
    current_index = 0
    while 1:
        if current_index >= len(icons) - 1:
            current_index = 0
        else:
            current_index += 1
        yield print(f'\r{icons[current_index]}', end='')


if __name__ == '__main__':
    a = spinner(icons=['🌑', '🌒', '🌓', '🌔', '🌕', '🌖', '🌗', '🌘'])
    max = 100
    for i in range(0, max):
        next(a)
        time.sleep(0.035)
    print('\r', end='')

    for i in range(0, max+1):
        bar(i, total=max, bar_length=20, show_percentage=True)
        time.sleep(0.035)
    print()
