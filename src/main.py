## Preliminary starting point for the whole program.
## The "actual stuff" is done in the agents and components themselves.

import os
import multiprocessing

## Start agents and workers here

## We'll need to fork the agents into their own processes as they'll be making
## blocking operations. If we try to run everything in a single process, we'll
## be blocking ourselves.

## Loop

  ## Poll agents here
  ## Use queues, as the data transfers is only one way: child -> parent, agent -> controller

  ## Pass sum of agent desires to plan executor here
