## This agent keeps track of changing electicity prices
## Outputs desire based on how much electricity costs at a given moment
## Desire output is between -1.0 to +1.0

## Electricity prices for a given next day are generally available at 14:30
## on a given day. We can use this data to predict future prices and optimize
## our pumping to times of low cost.

import requests

def electricity_tracker_agent(desire_output):
    