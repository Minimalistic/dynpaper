from time import sleep
from pendulum import now, DateTime, Duration

def pause_for(seconds: float):
    pause_until(now()+Duration(seconds=seconds), Duration(seconds=5))

def pause_until(target: DateTime, refresh: Duration):
    begin = now()
    while target.is_future() and (target-now()) > refresh:
        sleep(refresh.seconds)
        if begin.is_future():
            raise SysTimeModified()

class SysTimeModified(Exception):
    def __init__(self):
        super().__init__('Received begin time that is in future.')
