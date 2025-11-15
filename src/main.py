#!/usr/bin/env python3
## Preliminary starting point for the whole program.
## The "actual stuff" is done in the agents and components themselves.

import multiprocessing as mp
import time

import safety_compliance_enforcer as sce

if __name__ == '__main__':
## Start agents and workers here

  ## "Spawn" is the recommended method for Python
  ## Actual forking is more resource expensive
  mp.set_start_method('spawn')

  ## Safety compliance enforcer worker
  sce_read_socket = mp.Queue()
  safety_compliance_enforcer_worker = mp.Process(target= sce.safety_compliance_enforcer, args=(sce_read_socket,))
  safety_compliance_enforcer_worker.start()

  ## 

## Start safety-compliance-enforcer


## We'll need to fork the agents into their own processes as they'll be making
## blocking operations. If we try to run everything in a single process, we'll
## be blocking ourselves.

## Loop
  while True:
  ## Poll agents here
  ## Use queues, as the data transfers is only one way: child -> parent, i.e. agent -> controller
    print(sce_read_socket.get())
    time.sleep(1)
  ## Pass sum of agent desires to plan executor here
