## This worker is given a desire value by the agent controller.
## This worker's job is to then figure out the most optimal pump configuration
## to match the provided desire value, i.e. to pump as much as we need, but
## not a drop more.

## This worker will actually pass the 1 hour plans with 15 minute intervals to
## the pump controlling systems.

import time
import multiprocessing

def plan_executor(watcher_data_socket):
    while True:
        try:
            print(watcher_data_socket.recv())
        except EOFError:
            time.sleep(1)
        time.sleep(2)