import subprocess
import os.path
import time
import datetime
import socket
import yaml
from .desktop import set_wallpaper
from .desktop import get_desktop_environment
from .arguments import arguments
from sys import argv
import pendulum
import collections
from buzz import Buzz
from prettyprinter import cpprint as cprint
from . import timefstr
from . import abs_duration
from itertools import cycle

from typing import List, Tuple, Dict, Union, Generator


VERSION = '2.0.0a'


def get_version():
    return VERSION


def acquire_lock():
    __socket = socket.socket(
        socket.AF_UNIX, socket.SOCK_DGRAM)
    try:
        __socket.bind('\0'+'dynpaper')
    except socket.error:
        raise Buzz('Another instance is running.')
    return __socket


def singleTime(files: List, starttime: pendulum.Date, timeframe: pendulum.Duration=pendulum.duration(hours=24)):
    now = pendulum.now()
    delta = timeframe / len(files)
    wallpaper = None
    files = [files]
    index = (now - starttime) // delta
    remaining = (now - starttime) % delta
    yield files[index], remaining
    for wallpaper in files[index:]:
        yield wallpaper, delta


def generate_wallpapers(args: List):
    def inbetween(start, end, target):
        # Covers 10<13<15, start = 06:00, end = 04:00, target = 10:00
        return start < target < end or end < start < target
    if len(args) == 1:
        start = timefstr(args[0][time])
        while True:
            for wallpaper in singleTime(args[0]['files'], start):
                yield wallpaper

    now = pendulum.now()
    for x, y in zip(args, args[1:]):
        start = timefstr(x['time'])
        end = timefstr(y['time'])
        if not inbetween(start, end, now):
            continue
        else:  # After the first time in this part, it will always fall here.
            timeframe = abs_duration(start, end)
            for wallpaper in singleTime(x['files'], start, timeframe):
                yield wallpaper

    # Go to rest

    # Then go from beginning


def main(argv):
    try:
        __socket = acquire_lock()
        args = arguments(argv)
        denv = get_desktop_environment()
        wallpapers = generate_wallpapers(args)
        for timedelta, wallpaper in wallpapers:
            set_wallpaper(wallpaper, denv)
            time.sleep(timedelta.in_seconds())

    except Exception as e:
        print(e)
        if __socket:
            __socket.close()
