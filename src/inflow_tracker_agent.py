## This agent keeps track of amount of inflow into the storage tanks
## The more inflows we have, the more desire this agent outputs
## Output is between 0.0 and +1.0

import time
import random

def inflow_tracker_agent(desire_output):
    while True:
    ## For now, we only have placeholder code
    ## Later, we'll do the sensor polling here

    ## For now, we'll default to 0
        desire_output.put(random.random())
        time.sleep(5)