## Preliminary starting point for the whole program.
## The "actual stuff" is done in the agents and components themselves.

import os
import multiprocessing as mp

import safety_compliance_enforcer

if __name__ == '__main__':
## Start agents and workers here

  ## "Spawn" is the recommended method for Python
  ## Actual forking is more resource expensive
  mp.set_start_method('spawn')
  ## This queue is for reading data from the agents
  mp_queue = mp.Queue()

## Start safety-compliance-enforcer


## We'll need to fork the agents into their own processes as they'll be making
## blocking operations. If we try to run everything in a single process, we'll
## be blocking ourselves.

## Loop

  ## Poll agents here
  ## Use queues, as the data transfers is only one way: child -> parent, i.e. agent -> controller

  ## Pass sum of agent desires to plan executor here
