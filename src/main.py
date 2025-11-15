#!/usr/bin/env python3
## Preliminary starting point for the whole program.
## The "actual stuff" is done in the agents and components themselves.

import multiprocessing as mp
import time

import safety_compliance_enforcer as sce
import inflow_tracker_agent as ita

if __name__ == '__main__':
  ## Start agents and workers here
  ##
  ## We'll need to get the agents into their own processes as they'll be making
  ## blocking operations. If we try to run everything in a single process, we'll
  ## be blocking ourselves.

  ## "Spawn" is the recommended method for Python
  ## Actual "proper" forking is more expensive
  mp.set_start_method('spawn')

  ## Safety compliance enforcer worker start
  sce_read_socket = mp.Queue()
  safety_compliance_enforcer_worker = mp.Process(target= sce.safety_compliance_enforcer, args=(sce_read_socket,))
  safety_compliance_enforcer_worker.start()

  ## Inflow tracker agent start
  ita_read_socket = mp.Queue()
  inflow_tracker_agent = mp.Process(target= ita.inflow_tracker_agent, args=(ita_read_socket,))
  inflow_tracker_agent.start()

  ## Rain tracker agent start

  ## Electricity tracker agent start

  ## Storage tracker agent start

  ## Loop
  while True:
    ## Poll agents here
    ## Use queues, as the data transfers is only one way: child -> parent, i.e. agent -> controller
    
    ## For now, these calls are blocking, meaning we have to wait for all agents
    ## and workers to finish their sensor polling before we get an updated view
    ## of the system's state. This could be optimzed to be done in parallel.
    ##
    ## However, we elected not to do so for this concept, as the smallest unit
    ## of time we'll be working with is 15 minutes, as the pumps can't be controlled
    ## in any less amount of time.
    print(sce_read_socket.get())
    print(ita_read_socket.get())

    ## Simulate operations via sleep
    time.sleep(1)

    ## Pass agent states to plan executor
