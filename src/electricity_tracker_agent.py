## This agent keeps track of changing electicity prices
## Outputs desire based on how much electricity costs at a given moment
## Desire output is between -1.0 to +1.0

## Electricity prices for a given next day are generally available at 14:30
## on a given day. We can use this data to predict future prices and optimize
## our pumping to times of low cost.

import requests
import ast

def electricity_tracker_agent(desire_output):
    ## Fetch electricity prices from the simulation server
    upcoming_electricity_prices = requests.get("http://127.0.0.1:8000/all-upcoming-elec-price")
    upcoming_electricity_prices = upcoming_electricity_prices.text
    upcoming_electricity_prices = ast.literal_eval(upcoming_electricity_prices)
    upcoming_electricity_prices = [float(price) for price in upcoming_electricity_prices]
    print(upcoming_electricity_prices)

    ## Figure out highest price
    ## Figure out minimum price
    ## Assign relative desire values to other prices in comparison to max
    max_upcoming_price = max(upcoming_electricity_prices)
    min_upcoming_price = min(upcoming_electricity_prices)

    ## Find the price range for the upcoming 24 hours
    print(min_upcoming_price)
    print(max_upcoming_price)
    price_range = float(max_upcoming_price) - float(min_upcoming_price)
    ## Find the median price of the upcoming 24 hours
    sorted_prices = sorted(upcoming_electricity_prices)
    n = len(sorted_prices)
    if n % 2 == 0:
        mid_price = (float(sorted_prices[n//2 - 1]) + float(sorted_prices[n//2])) / 2
    else:
        mid_price = float(sorted_prices[n//2])

    ## Compare the current hour price to upcoming price to see how desirable
    ## pumping right now is.
    current_price = float(upcoming_electricity_prices[0])
    
    if current_price <= min_upcoming_price:
        pumping_desire = 1.0
    elif current_price >= max_upcoming_price:
        pumping_desire = -1.0
    elif current_price < mid_price:
        ## Scale from +1.0 (at min) to 0 (at median)
        pumping_desire = 1.0 - (current_price - min_upcoming_price) / (mid_price - min_upcoming_price)
    else:
        ## Scale from 0 (at median) to -1.0 (at max)
        pumping_desire = -(current_price - mid_price) / (max_upcoming_price - mid_price)

    ## Output pumping desire to agent watcher
    #desire_output.put(pumping_desire)

    ## DEBUG: print
    print(pumping_desire)

# electricity_tracker_agent(None)
# outflow_request = {"outflow":1}
# requests.post("http://127.0.0.1:8000/outflow", json=outflow_request, timeout=5)