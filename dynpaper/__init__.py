from dynpaper import main as dpmain
from pendulum import from_format as timefstr
from pendulum import duration
from functools import partial
from pendulum import Date

timefstr = partial(timefstr, fmt='HH:mm')


def abs_duration(start: Date, end: Date):
    """
    For the function to provide the expected result
    """
    if start < end:
        return end - start
    else:
        return duration(hours=24) - start + end


def main():
    from sys import argv
    dpmain(argv)
