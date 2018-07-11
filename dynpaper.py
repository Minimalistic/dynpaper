#!/usr/bin/env python3

import subprocess
import os.path
import time
import datetime
import socket
import yaml
from process_calls import PROCESS_CALLS
from arguments import arguments
from sys import argv

VERSION = '2.0.0a'

def get_version():
    return VERSION


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

def add_to_shell(args, argv):

    argv = [x for x in argv[1:] if x not in {
        '-s', '--shell-conf', args.shell_conf, '-a', '--auto-run'}]

    runf = "dynpaper "
    for arg in argv:
        runf = runf+' {}'.format(arg)
    runf = runf + ' &\n'

    with open(args.shell_conf, 'r') as fp:
        content = fp.readlines()
        fp.close()

    if '#dynpaper\n' in content:
        index = content.index('#dynpaper\n')
        if index == len(content):
            content.append(runf)
        else:
            content[index + 1] = runf
    else:
        content.append('#dynpaper\n')
        content.append(runf)

    with open(args.shell_conf, 'w') as fp:
        fp.writelines(content)
        fp.close()

    return


def get_index(args):

    dawn_time = args.dawn
    dusk_time = args.dusk

    current_time = time_string_to_float('{}:{}'.format(
        datetime.datetime.now().hour, datetime.datetime.now().minute))
    day_dur = dusk_time-dawn_time
    night_duration = 24.0 - day_dur

    day_size = args.file_range[0]
    night_size = args.file_range[1]-day_size-1

    if dawn_time+day_dur >= current_time and current_time >= dawn_time:
        # It's day
        index = (current_time - dawn_time)/(day_dur/day_size)
    else:
        # It's night
        if current_time > dawn_time:
            index = day_size + (current_time-day_dur -
                                dawn_time)/(night_duration/night_size)
        else:
            index = day_size + (current_time + 23-dawn_time-day_dur) / \
                (night_duration/night_size)
    return int(index+1)


def set_wallpaper(args):
    index = get_index(args)
    subprocess.run(PROCESS_CALLS[args.env].format_map(
        {'file':args.file_template.format(index)}), shell=True)

def acquire_lock():
    __socket = socket.socket(
        socket.AF_UNIX, socket.SOCK_DGRAM)
    try:
        __socket.bind('\0'+'dynpaper')
    except socket.error:
        print('Already running.')
        exit(-1)
    return __socket


def main():
    __socket = acquire_lock()
    args = arguments()
    if args.auto_run:
        add_to_shell(args, argv)

    args.dawn = time_string_to_float(args.dawn)
    args.dusk = time_string_to_float(args.dusk)

    index = get_index(args)

    while True:
        set_wallpaper(args)
        while index == get_index(args):
            time.sleep(args.interval)
        index = get_index(args)


if __name__ == '__main__':
    main()
