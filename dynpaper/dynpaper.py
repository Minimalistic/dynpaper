from itertools import cycle
from collections import deque

from pendulum import duration, now, from_format
from pendulum import time
from tendo import singleton

from .arguments import arguments
from .desktop import get_desktop_environment, set_wallpaper
from .pause import SysTimeModified, pause_until


def timefstr(string):
    t = from_format(string, fmt='HH:mm', tz=now().tz)
    return t


def astime(x): return time(x.hour, x.minute, x.second)


def generate_wallpapers(args):

    if len(args) == 1:
        start = timefstr(args[0]['time'])
        files = args[0]['files']
        delta = duration(hours=24)/len(files)
        interval = duration(hours=24)
        files = [[wallpaper, start+(delta*(indx+1))]
                 for indx, wallpaper in enumerate(files)]
    else:
        files = []
        rotated = [x for x in args[1:]]
        rotated.append(args[0])

        timefstr(args[0]['time'])
        start = timefstr(args[0]['time'])
        for current, nxt in zip(args, rotated):
            cfiles = current['files']
            ct = timefstr(current['time'])
            nt = timefstr(nxt['time'])
            nt += duration(hours=24 * (nt < ct))
            delta = (nt - ct) / len(cfiles)
            files.extend([[wallpaper, start + (delta * (indx+1))]
                          for indx, wallpaper in enumerate(cfiles)])
            start += (nt - ct)

        interval = start
    return wallpaper_wrapper(files, interval)


def wallpaper_wrapper(wallpapers, interval):
    """
    This function builds and returns 2 functions that manage the generated 
    wallpapers. The wallpapers parameter is a list of two item lists 
    (Lists are mutable, tuples not), where the first element is the path to 
    the wallpaper, the second element is the target datetime. The items in 
    the list in the expected order of usage. If the current time is __not__ available,
    the items at the end of the list are rotated to the front and have their target datetime updated.

    The sync function is used to keep the wallpapers in sync and return the wallpaper appropriate for
    the time.

    The reset function is used to reset the wallpaper list that sync uses to the initial state and resync.
    Under __regular__ usage, reset function is __never__ called. If however, the user needs to change the time
    to an earlier datetime, the reset function is to be called.
    """

    og = [[x[0], x[1]] for x in wallpapers]
    objs = [og, deque(wallpapers)]

    def sync():
        wallpapers = objs[1]
        now()

        while (wallpapers[-1][1] - interval).is_future():
            wallpapers[-1][1] = wallpapers[-1][1] - interval
            wallpapers.rotate(1)

        while (wallpapers[0][1]).is_past():
            wallpapers[0][1] = wallpapers[0][1] + interval
            wallpapers.rotate(-1)

        return wallpapers[0]

    def reset():
        objs[1] = deque([[x[0], x[1]] for x in objs[0]])

    return sync, reset


def main(argv):
    try:
        me = singleton.SingleInstance()  # will sys.exit(-1) if other instance is runnin
    except singleton.SingleInstanceException:
        exit(-1)
    try:
        args = arguments(argv)
        sync_wallpapers, reset_wallpapers = generate_wallpapers(args)
        while True:
            wallpaper, target = sync_wallpapers()
            set_wallpaper(wallpaper)
            try:
                pause_until(target)
            except SysTimeModified:
                """
                This error is raised when the clock is at a time earlier than the time it began to pause.
                This indicates a hard/manual clock change. In order to keep the program running and in
                defined state, the wallpapers list is reset through 'reset_wallpapers' and gets resynced by
                sync_wallpapers function.
                """
                reset_wallpapers()
    except ValueError as e:
        print(e)
        __socket.close()
        return


if __name__ == '__main__':
    from sys import argv
    main(argv)
