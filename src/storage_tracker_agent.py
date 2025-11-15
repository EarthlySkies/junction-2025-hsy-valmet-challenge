## This agent keeps track of the storage water level
## Output more desire the more storage is used
## Desire output is between 0.0 to +1.0

## The job of this agent to prevent the storage from overflowing. Thus, it
## simply increases its desire as the water level rises in the storage.

import requests

def storage_tracker_agent(desire_output):
    ## Fetch storage level
    current_water_level = requests.get("http://127.0.0.1:8000/water-level")
    ## DEBUG: print
    print("Current water level: ", current_water_level.text)

    ## Water level should always be below 7.5 meters to stay within pre-approved
    ## safety margins, as 8.0 is L1 MAX. It should also remain above 0.0, as that
    ## is L1 MIN.

    ## Calculate our pumping desire based on used storage
    ## This is to catch any malformed water level data beyond normal regulations
    if float(current_water_level.text) < 0:
        pumping_desire = 0
    elif float(current_water_level.text) > 8:
        pumping_desire = 1
    else:
        ## Else we simply take the percentage of the water level
        pumping_desire = float(current_water_level.text) / 8

    ## Output pumping desire to agent watcher
    desire_output.put(pumping_desire)

    ## Advance water level simulation
    outflow_request = {"outflow":1}
    requests.post("http://127.0.0.1:8000/outflow", json=outflow_request, timeout=5)
