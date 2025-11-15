## Preliminary starting point for the whole program.
## The "actual stuff" is done in the agents and components themselves.

import os

## Start agents and components here

## Start watcher here

## Poll agents here (loop)

## Pass sum of agent desires to plan executor


### Interacting with the simulation 

import requests

outflow = {
    "outflow": 1.0,
}

#each 15 minutes yo
pass_15_min = requests.post("http://127.0.0.1:8000/outflow", json=outflow, timeout=5)

current_water_level = requests.get("http://127.0.0.1:8000/water-level")

#rain in 15 min
next_rain = requests.get("http://127.0.0.1:8000/next-rain")

#elec at current time
current_elec_price = requests.get("http://127.0.0.1:8000/current-elec-price")

#elec prices in the future
all_upcoming_elec_price = requests.get("http://127.0.0.1:8000/all-upcoming-elec-price")




