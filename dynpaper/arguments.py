
import os
import argparse
import pendulum
import yaml

from buzz import Buzz
from functools import reduce
from schemas import validate_config

DEFAULT_PATH = os.path.expanduser('~/.config/dynpaper/config')


def load_args(args):
    if args.file:
        with open(args.file, 'r') as fp:
            args = yaml.load(fp)
        try:
            args = validate_config(args)
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
