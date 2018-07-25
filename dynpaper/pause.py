from time import sleep
from pendulum import now as now, time, Duration



    

def pause_for(seconds: float):
    pause_until(now()+Duration(seconds=seconds))


def pause_until(target, refresh: Duration = Duration(seconds=1)):
    begin = now()
    while target.is_future():
        if begin.is_future():
            raise SysTimeModified()
        else:
            sleep(refresh.in_seconds())



class SysTimeModified(Exception):
    def __init__(self):
        super().__init__('Received begin time that is in future.')
