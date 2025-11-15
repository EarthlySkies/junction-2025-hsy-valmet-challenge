## This agent keeps track of the storage water level
## Output more desire the more storage is used
## Output is between 0.0 to +1.0

## The job of this agent to prevent the storage from overflowing. Thus, it
## simply increases its desire as the water level rises in the storage.

import requests

def storage_tracker_agent(desire_output):
    ## Fetch storage level
    current_water_level = requests.get("http://127.0.0.1:8000/water-level")
    ## DEBUG: print
    print(current_water_level)

    ## Water level should always be below 7.5 meters to stay within pre-approved
    ## safety margins, as 8.0 is L1 MAX. It should also remain above 0.5, as that
    ## is L1 MIN.

    ## Calculate our pumping desire

    #pumping_desire = 7 - current_water_level

    ## Output pumping desire
    desire_output.put()

    ## Advance water level simulation
    requests.post("http://127.0.0.1:8000/outflow")
