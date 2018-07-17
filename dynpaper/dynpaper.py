#!/usr/bin/env python3

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


def sync_wallpapers(dawn, wallpapers):
    """
    sync_wallpapers syncs the wallpapers with the time, such that
    wallpapers[0] is the wallpaper that is supposed to be shown now.

    rotate wallpapers is to be used every time the process wakes, the reason is that the computer might sleep
    and wake up much later than the sleep duration, thus, to keep the process sync with outside world,
    sync_wallpapers is called right after the time.sleep call.
    """
    wallpapers = collections.deque(
        wallpapers)  # Clone, in order to keep the original list intact and in order.

    delta = pendulum.duration(seconds=(pendulum.now()-dawn).in_seconds())
    # The first wallpaper is that of dawn, wallpapers[0] is a pair where first is uptime. second is file.
    diff = wallpapers[0][0]
    while delta > pendulum.duration(0):
        delta -= diff
        wallpapers.rotate(-1)
        diff = wallpapers[0][0]

    # The duration for the current wallpaper
    return diff - delta, wallpapers[0][1]


def main(argv):
    try:
        __socket = acquire_lock()
        args = arguments(argv)
        denv = get_desktop_environment()
        wallpapers = args['wallpapers']
        dawn = args['dawn']
        timedelta, wallpaper = sync_wallpapers(dawn, wallpapers)
        while True:
            set_wallpaper(wallpaper, denv)
            time.sleep(timedelta.in_seconds())
            timedelta, wallpaper = sync_wallpapers(dawn, wallpapers)

    except Exception as e:
        print(e)
        if __socket:
            __socket.close()
