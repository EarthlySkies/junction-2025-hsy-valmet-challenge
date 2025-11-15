#!/usr/bin/env python3
## Preliminary starting point for the whole program.
## The "actual stuff" is done in the agents and components themselves.

import multiprocessing as mp
import time

import safety_compliance_enforcer as sce
import inflow_tracker_agent as ita
import electricity_tracker_agent as eta
import storage_tracker_agent as sta
import plan_executor as pa

if __name__ == '__main__':
  ## "Spawn" is the recommended method for Python
  ## Actual "proper" forking is more expensive
  mp.set_start_method('spawn')

  ## Loop
  while True:
    ## Start agents and workers here
    ## We'll need to get the agents into their own processes as they'll be making
    ## blocking operations. If we try to run everything in a single process, we'll
    ## be blocking ourselves.

    ## Safety compliance enforcer worker start
    sce_read_socket = mp.Queue()
    safety_compliance_enforcer_worker = mp.Process(target= sce.safety_compliance_enforcer, args=(sce_read_socket,))
    safety_compliance_enforcer_worker.start()

    ## Inflow tracker agent start
    #ita_read_socket = mp.Queue()
    #inflow_tracker_agent = mp.Process(target= ita.inflow_tracker_agent, args=(ita_read_socket,))
    #inflow_tracker_agent.start()

    ## Rain tracker agent start

    ## Electricity tracker agent start
    eta_read_socket = mp.Queue()
    electricity_tracker_agent = mp.Process(target= eta.electricity_tracker_agent, args=(eta_read_socket,))
    electricity_tracker_agent.start()

    ## Plan executor start
    ## This needs to be a pipe as we'll need to write data to the executor (a child)
    #pa_write_socket, pa_read_socket = mp.Pipe()
    #plan_executor = mp.Process(target= pa.plan_executor, args=(pa_read_socket,))
    #plan_executor.start()

    ## Storage tracker agent start
    sta_read_socket = mp.Queue()
    storage_tracker_agent = mp.Process(target= sta.storage_tracker_agent, args=(sta_read_socket,))
    storage_tracker_agent.start()

    ## Poll agents here
    ## Use queues, as the data transfers is only one way: child -> parent, i.e. agent -> controller
    
    ## For now, these calls are blocking, meaning we have to wait for all agents
    ## and workers to finish their sensor polling before we get an updated view
    ## of the system's state. This could be optimzed to be done in parallel.
    ##
    ## However, we elected not to do so for this concept, as the smallest unit
    ## of time we'll be working with is 15 minutes, as the pumps can't be controlled
    ## in any less amount of time.

    ## Agent desire list
    agent_desire_list = []

    #agent_desire_list.append(sce_read_socket.get())
    #agent_desire_list.append([ita_read_socket.get()])
    agent_desire_list.append(eta_read_socket.get())
    agent_desire_list.append(sta_read_socket.get())

    ## Pass agent states to plan executor
    #pa_write_socket.send(agent_desire_list)
    #pa_write_socket.close()
    #plan_executor.join()

    ## Enforce safety limits
    if float(sce_read_socket.get()) == 1:
      ## TODO: Pumps on at max here
      ## Skip the rest of the agent desire evaluations as we're in an emergency
      continue

    ## TODO: Add tunnel emptier times here
    ## Basically call the function and print the output to stdout

    ## TODO: Activate pumps here

    ## TODO: Write pump activations to stdout as a list
    ## Index 0-5 is big pumps, index 6-7 is small pumps
    ## List contains the current operating level of the pumps as 0-100 floats

    ## DEBUG: print 
    print(agent_desire_list)

    ## Simulate operations via sleep
    ## Placeholder code for now
    time.sleep(1)
