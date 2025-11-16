#!/usr/bin/env python3
## Preliminary starting point for the whole program.
## The "actual stuff" is done in the agents and components themselves.

import requests
import multiprocessing as mp
import time

#import safety_compliance_enforcer as sce

import storage_tracker_agent as sta
import electricity_tracker_agent as eta

if __name__ == '__main__':
  ## "Spawn" is the recommended method for Python
  ## Actual "proper" forking is more expensive
  mp.set_start_method('spawn')

  ## Our default pump statuses which we start with
  ## This list keeps track of which pump is operating at what capacity
  ## Index 0-5 is big pumps, index 6-7 is small pumps
  ## List contains the current operating level of the pumps as 0-100 floats
  ## We start with defaulting to one small pump on, as one pump must be operational
  ## at all times regardless of flow.
  pump_status_list = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 100.0]
  
  


  ## Loop
  while True:

    ## Safety compliance enforcer worker start
     #sce()
    # safety_compliance_enforcer_worker = mp.Process(target= sce.safety_compliance_enforcer, args=(sce_read_socket,))
    # safety_compliance_enforcer_worker.start()

    ## Electricity tracker agent start
    eta_read_socket = mp.Queue()
    electricity_tracker_agent = mp.Process(target= eta.electricity_tracker_agent, args=(eta_read_socket,))
    electricity_tracker_agent.start()

    # ## Storage tracker agent start
    sta_read_socket = mp.Queue()
    storage_tracker_agent = mp.Process(target= sta.storage_tracker_agent, args=(sta_read_socket,))
    storage_tracker_agent.start()



    agent_desire_list = []

    agent_desire_list.append(eta_read_socket.get())
    agent_desire_list.append(sta_read_socket.get())

    print("The desire list is")
    print(agent_desire_list)
   
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

    ## We must keep track of the water outflows from L1
    total_outflow = 0

    for x in pump_status_list:
      if x == 100.0:
        total_outflow = total_outflow + 1.0
      
    ## Update simulation server outputs; we'll read them during the next loop
    outflow_request = {"outflow": total_outflow}
    requests.post("http://127.0.0.1:8000/outflow", json=outflow_request, timeout=5)

    current_water_level = float(requests.get("http://127.0.0.1:8000/water-level").text)

    if current_water_level < 20:
      agent_desire_list[0] = agent_desire_list[0] * 0.5


    if (agent_desire_list[0] + agent_desire_list[1]) > 1.1:
      pump_status_list = switch_first_zero(pump_status_list)
      print("added pump")
    if(agent_desire_list[0]+ agent_desire_list[1]) < 0.7:
      pump_status_list = switch_last_one_back(pump_status_list)
      print("removed pump")
    elif agent_desire_list[1] == 0:
      pump_status_list = switch_last_one_back(pump_status_list)
      print("removed pump")

    if current_water_level <= 15:
      pump_status_list = [100.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
    elif current_water_level >= 110:  
      pump_status_list = [100.0, 100.0, 100.0, 100.0, 100.0, 100.0, 0.0, 0.0]


    ## Write pump activations to stdout as a list
    print("Pump activation statuses:")
    print(pump_status_list)

    ## Simulate operations via sleep
    ## Placeholder code for now
    time.sleep(1)
