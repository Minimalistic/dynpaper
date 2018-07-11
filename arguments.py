from process_calls import PROCESS_CALLS
from sys import argv
import os
import argparse

def arguments():
    parser = argparse.ArgumentParser()

    parser.add_argument('-a', '--auto-run',
                        default=False, action='store_const', const=True, help='Turn flag on to add\
                         shell command in your shell config file, default is ~/.profile, provide specific with -s')
    parser.add_argument('-f', '--file-template',
                        action='store', type=str, help='File template for the wallpapers,\
                         ex. \'~/Pictures/Wallpapers/mojave_dynamic_{}.png\', use \'{}\' to replace the number.')
    parser.add_argument('-s', '--shell-conf', action='store', default='~/.profile',
                        help='The config of the shell you are using, ~/.profile for bash, ~/.zprofile for zsh etc.')
    parser.add_argument('-r', '--dawn', action='store',
                        default='06:00', help='Dawn/sunrise time, ex. 06:23')
    parser.add_argument('-d', '--dusk', action='store',
                        default='20:00', help='Dusk/sunset time, ex. 20:23')
    parser.add_argument(
        '-e', '--env', choices=PROCESS_CALLS.keys(), required=True, help='Your current desktop environment/wallpaper manager.')
    parser.add_argument('-i', '--interval', action='store', type=int,
                        default=300, help='Refresh interval in seconds, default = 300.')

    parser.add_argument(
        '-g', '--file-range', action='store', default='(13,17)', help='File index range. Ex (13,17) indicates the files [1,12]\
         inclusive are split throughout the day and the files[13, 16] inclusive are split throughout the night.If you are using\
          apple\'s wallpapers, don\'t set it.')

    args = parser.parse_args(argv[1:])

    err_range(args)
    err_dusk_dawn(args)
    err_set_auto(args)
    err_wallpapers(args)
    err_interval(args)

    return args


def err_interval(args):
    try:
        if not isinstance(args.interval, int):
            raise ValueError
        if args.interval < 1:
            raise ValueError
    except:
        print('Interval needs to be an integer greater than 1')


def err_range(args):
    try:
        args.file_range = eval(args.file_range)
        if not isinstance(args.file_range, tuple):
            raise ValueError
        if args.file_range[0] > args.file_range[1]:
            raise ValueError
        if not isinstance(args.file_range[0], int):
            raise ValueError
        if not isinstance(args.file_range[1], int):
            raise ValueError
    except:
        print(
            'Invalid format specified, please use x,y or (x,y) where x<y, x,y are integers.')
        exit(-1)


def err_wallpapers(args):
    for i in range(1, args.file_range[1]):
        file = args.file_template.format(i)
        if not os.path.isfile(file):
            print('File:{} does not exist.'.format(file))
            exit(-1)


def time_string_to_float(time):
    if ':' not in time:
        return 'Should be in form HH:mm.'
    time = time.split(':')
    if len(time) != 2:
        return 'Should be in this form: HH:mm.'

    try:

        hours = int(time[0])
    except:
        return 'Hours should be an int.'

    if not (0 <= hours <= 23):
        return 'Hours should be in range [0,23].'

    try:
        minutes = int(time[1])
    except:
        return 'Minutes should be an int.'

    if not (0 <= minutes < 60):
        return 'Minutes should be in range [0,23].'

    return hours+minutes/60.0


def err_set_auto(args):
    if not args.auto_run:
        return

    if not os.path.isfile(args.shell_conf):
        print('Shell config file:{} doesn\'t exist.'.format(args.shell_conf))
        exit(-1)



def err_dusk_dawn(args):

    dawn_time = time_string_to_float(args.dawn)
    if isinstance(dawn_time, str):
        print('Dawn time is invalid, err: {}'.format(dawn_time))
        exit(-1)

    dusk_time = time_string_to_float(args.dusk)
    if isinstance(dusk_time, str):
        print('Dusk time is invalid, err: {}'.format(dusk_time))
        exit(-1)

    if time_string_to_float(args.dawn) > time_string_to_float(args.dusk):
        print('Dawn can\'t be after dusk.')
        exit(-1)

    pass