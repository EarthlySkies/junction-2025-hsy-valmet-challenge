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
    ## Find the middle point of the 24 hours
    mid_price = float(min_upcoming_price) + price_range / 2

    ## Compare the current hour price to upcoming price to see how desirable
    ## pumping right now is.
    if upcoming_electricity_prices[0] <= min_upcoming_price:
        pumping_desire = 1.0
    elif upcoming_electricity_prices[0] >= max_upcoming_price:
        pumping_desire = -1.0
    elif float(upcoming_electricity_prices[0]) < mid_price:
        pumping_desire = float(min_upcoming_price) / float(upcoming_electricity_prices[0])
    else:
        pumping_desire = float(upcoming_electricity_prices[0]) / float(max_upcoming_price)

    ## Get the actual pumping desire
    pumping_desire = pumping_desire / float(max_upcoming_price)

    ## Output pumping desire to agent watcher
    desire_output.put(pumping_desire)

    ## DEBUG: print
    print(pumping_desire)