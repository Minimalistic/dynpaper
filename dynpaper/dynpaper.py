from itertools import cycle
from sys import stderr
from collections import deque

from pendulum import duration, now, from_format
from tendo import singleton

from arguments import arguments
from desktop import get_desktop_environment, set_wallpaper
from pause import SysTimeModified, pause_until


def timefstr(string): return from_format(
    string, fmt='HH:mm', tz=now().tz)


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

        start0 = timefstr(args[0]['time'])
        start = timefstr(args[0]['time'])
        for current, nxt in zip(args, rotated):
            cfiles = current['files']
            ct = timefstr(current['time'])
            nt = timefstr(nxt['time'])
            nt += duration(hours=24 * (nt < ct))
            delta = (nt - ct) / len(cfiles)
            files.extend([[wallpaper, start + (delta * (indx+1))]
                          for indx, wallpaper in enumerate(cfiles)])
            start += (nt-ct)

        interval = duration(seconds=(start - start0).in_seconds())

    while files[0][1].is_future():
        files = [x for x in map(lambda f:[f[0], f[1] - interval], files)]

    return interval, files


def main(argv):
    try:
        me = singleton.SingleInstance()  # will sys.exit(-1) if other instance is runnin
    except singleton.SingleInstanceException:
        exit(-1)
    try:
        args = arguments(argv)
        delta, wallpapers = generate_wallpapers(args)
        wallpapers = deque(wallpapers)
        # Sync
        while wallpapers[0][1].is_past():
            wallpapers[0][1] = wallpapers[0][1].add(seconds=delta.seconds)
            wallpapers.rotate(-1)
        while True:
            wallpapers[0][1] = wallpapers[0][1].add(seconds=delta.seconds)
            set_wallpaper(wallpapers[0][0])
            try:
                pause_until(wallpapers[0][1])
                wallpapers.rotate(-1)
            except SysTimeModified as e:
                print(e, file=stderr)
                while (wallpapers[0][1] - delta).is_future():
                    wallpapers.rotate(1)
                    wallpapers[0][1] = wallpapers[0][1].add(seconds=-delta.seconds)

    except ValueError as e:
        print(e)
        __socket.close()
        return


if __name__ == '__main__':
    from sys import argv
    main(argv)
