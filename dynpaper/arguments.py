
import os
import argparse
import pendulum
import yaml

from buzz import Buzz
from dynpaper.process_calls import PROCESS_CALLS
from functools import reduce
from .schemas import *

DEFAULT_PATH = os.path.expanduser('~/.config/dynpaper/config')


def load_args(args):
    if args.file:
        with open(args.file, 'r') as fp:
            args = yaml.load(fp)
        try:
            SCH_CONFIG.validate(args)
            args['dawn'] = pendulum.from_format(args['dawn'], 'HH:mm')
            args['dusk'] = pendulum.from_format(args['dusk'], 'HH:mm')
            Buzz.require_condition(
                args['dawn'] < args['dusk'], 'Dawn has to be before Dusk.')
        except Exception as e:
            raise Buzz(
                f'Exception: {e}\n\n\nSchema validation error. Please make sure all the provided files exist!.')
        return args

    elif args.init:
        if not os.path.exists(DEFAULT_PATH):
            os.makedirs(DEFAULT_PATH[:DEFAULT_PATH.rindex('config')])
        with open(DEFAULT_PATH, 'w') as fp:
            yaml.dump(DEFAULT_CONFIG, fp, default_flow_style=False)

        raise Buzz(
            'We have created a new file here: {DEFAULT_PATH}, please update it and run dynpaper again.', DEFAULT_PATH=DEFAULT_PATH)

    else:
        raise Buzz('Unknown message occured.')


def generate_wallpapers(args):
    def gen_wallpapers(val):
        files = []
        if 'files' in val:
            files = val['files']

        if 'template' in val:
            rnge = val['range']
            temp = val['template']['path']
            files = [temp.format(i) for i in range(*eval(rnge))]

        return files

    dawn = args['dawn']
    dusk = args['dusk']
    day_dur = dusk - dawn
    night_dur = pendulum.duration(hours=24)-day_dur

    day_files = gen_wallpapers(args['wallpapers']['day'])
    day_dur /= len(day_files)
    day_files = [(day_dur, file) for file in day_files]

    night_files = gen_wallpapers(args['wallpapers']['night'])
    night_dur /= len(night_files)
    night_files = [(night_dur, file) for file in night_files]

    day_files.extend(night_files)
    return day_files


def arguments(argv):
    parser = argparse.ArgumentParser()

    mutexgroup = parser.add_mutually_exclusive_group()
    mutexgroup.add_argument('-i', '--init',
                            action='store_true',
                            default=False,
                            help='Create a sample config file at ~/.config/dynpaper/config or specify your own location')
    mutexgroup.add_argument('-f', '--file', action='store')

    args = parser.parse_args(argv[1:])

    Buzz.require_condition(any(args.__dict__.values()),
                           'No arguments provided.')

    args = load_args(args)

    return args
