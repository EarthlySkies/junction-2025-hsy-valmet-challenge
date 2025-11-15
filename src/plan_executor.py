## This worker is given a desire value by the agent controller.
## This worker's job is to then figure out the most optimal pump configuration
## to match the provided desire value, i.e. to pump as much as we need, but
## not a drop more.

## This worker will actually pass the 1 hour plans with 15 minute intervals to
## the pump controlling systems.

import time
import multiprocessing
import request
from typing import Dict, List

def plan_executor(watcher_data_socket):
    PUMP_IDS: Dict[str, float]={
        "Pump 1.1": 0,
        "Pump 1.2": 0,
        "Pump 1.3": 0,
        "Pump 1.4": 0,
        "Pump 2.1": 0,
        "Pump 2.2": 0,
        "Pump 2.3": 0,
        "Pump 2.4": 0,
    }
    while True:
        try:
            print(watcher_data_socket.recv())
        except EOFError:
            time.sleep(1)
        time.sleep(2)
        # 
        current_pump_statuses = requests.get("http://127.0.0.1:8000/pump-statuses")
        for id in PUMP_IDS:
            if current_pump_statuses[id] != 0:
                PUMP_IDS[id] += 0.25
        
        