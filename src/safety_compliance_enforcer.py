## This component ensures that the system operates within predefined safety
## margins.

## Basically, we need to make sure at least one pump is running at all times
## and that our storage tunnel (L1) is never filled beyond full capacity.

## If the storage capacity is exceeded beyond a pre-defined safe operating
## limit, this enforcer will ensure more pumps are activated to prevent
## overflows and safety limits.

## When the system is operating wihtin safe limits, this worker does not
## care about optimization, and thus stays silent.

## This worker has three states:
## -1: Reduce pumping to minimum
##  0: No output (see note above)
## +1: Pump at maximum

import time
import requests

def safety_compliance_enforcer(enforcer_state):
    ## This is the state of the enforcer
    ## Acceptable values are -1, 0, +1

    ## In this loop, we poll "various sensors" to ensure that the system is operating
    ## within predefined safety margins. If the system passes a safety marging,
    ## we respond to it by either halting the pumps or pumping at maximum capacity,
    ## depending on the kind of safety hazard we're experiencing.

    while True:
        ## For now, we only have placeholder code
        ## Later, we'll do the sensor polling here

        ## Get simulated water level
        current_water_level = requests.get("http://127.0.0.1:8000/water-level")
        current_water_level = float(current_water_level.text)

        ## Default to no emergency
        emergency = 0
        if current_water_level > 110:
            emergency = 1
        
        ## Pass the enforcement value to main
        enforcer_state.put(emergency)

        time.sleep(1)