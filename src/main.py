#!/usr/bin/env python3
## Preliminary starting point for the whole program.
## The "actual stuff" is done in the agents and components themselves.

import requests
import multiprocessing as mp
import time

import safety_compliance_enforcer as sce
import inflow_tracker_agent as ita
import electricity_tracker_agent as eta
import storage_tracker_agent as sta
import plan_executor as pa
import tunnel_emptier as te

if __name__ == '__main__':
  ## "Spawn" is the recommended method for Python
  ## Actual "proper" forking is more expensive
  mp.set_start_method('spawn')

  pump_status_list = [100.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
  
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

    ## Advance the simulated data values to their next iterations
    
    ## Poll agents here
    ## Use queues, as the data transfers is only one way: child -> parent, i.e. agent -> controller
    
    ## For now, these calls are blocking, meaning we have to wait for all agents
    ## and workers to finish their "sensor polling" before we get an updated view
    ## of the system's state. This is done in parallel in dedicated processes for optimization.
    ##
    ## However, we elected not to do so for this concept, as the smallest unit
    ## of time we'll be working with is 15 minutes, as the pumps can't be controlled
    ## in any less amount of time.

    ## Agent desire list. This contains all the desire outputs of agents
    agent_desire_list = []

    #agent_desire_list.append(sce_read_socket.get())
    #agent_desire_list.append([ita_read_socket.get()])
    agent_desire_list.append(eta_read_socket.get())
    agent_desire_list.append(sta_read_socket.get())

    print("The desire list is")
    print(agent_desire_list)
    ## Pass agent states to plan executor
    #pa_write_socket.send(agent_desire_list)
    #pa_write_socket.close()
    #plan_executor.join()

    ## Pump status list
    ## Index 0-5 is big pumps, index 6-7 is small pumps
    ## List contains the current operating level of the pumps as 0-100 floats
    ## Last element is 100 by default as we must have at least one pump active
    ## at all times.
    

    ## Enforce safety limits
    ## 1 is if the L1 tunnel is close to flooding out completely
    sce_status = float(sce_read_socket.get())
    if sce_status == 1:
      ## Power on as many pumps as possible to prevent L1 from flooding. We don't
      ## want wastewater ending up at the streets so we pump despite the costs it
      ## may incur.
      pump_status_list = [100.0, 100.0, 100.0, 100.0, 100.0, 0.0, 0.0, 0.0]
      ## Skip the rest of the agent desire evaluations as we're in an emergency
      print(pump_status_list)
      continue
    elif sce_status == -1:
      ## This is for when L2 is threatening to flood. We put the pumps to minumum
      ## to give time for the WWTP to deal with the water in L2 before pushing more in.
      ## In this current state, the SCE currently never reaches this value.
      ##
      ## We can continue straight away as our default configuration is to pump at
      ## minumum capacity, i.e. one small pump.
      continue
    
    ## Output our projected tunnel empty times to stdout
    ## These values are based on the data the program is given in a single simulation
    ## cycle and might not ever be reached with set of simulated data.
    # tunnel_empty_timestamps = te.optimal_tunnelwindow()
    # print("Tunnel emptying starts at:")
    # print(tunnel_empty_timestamps[0])
    # print("Tunnel will be empty by:")
    # print(tunnel_empty_timestamps[1])

    ## TODO: Activate pumps here based on desire
    def switch_first_zero(arr):
      for i, v in enumerate(arr):
        if v == 0.0:
            arr[i] = 100.0
            break
      return arr
    
    def switch_last_one_back(arr):
      # go from the back to the front
      for i in range(len(arr) - 1, -1, -1):
        if arr[i] == 100.0 and i != 0:
            arr[i] = 0.0
            break
      return arr

    total_outflow = 0
    for x in pump_status_list:
      if x == 100.0:
        total_outflow = total_outflow + 1.0
      
    outflow_request = {"outflow": total_outflow}
    requests.post("http://127.0.0.1:8000/outflow", json=outflow_request, timeout=5)


    if (agent_desire_list[0] + agent_desire_list[1]) > 1.1:
      pump_status_list = switch_first_zero(pump_status_list)
      print("added pump")
    if(agent_desire_list[0]+ agent_desire_list[1]) < 0.7:
      pump_status_list = switch_last_one_back(pump_status_list)
      print("removed pump")
    elif agent_desire_list[1] == 0:
      pump_status_list = switch_last_one_back(pump_status_list)
      print("removed pump")


    ## Write pump activations to stdout as a list
    print("Pump activation statuses:")
    print(pump_status_list)

    ## Simulate operations via sleep
    ## Placeholder code for now
    time.sleep(1)
