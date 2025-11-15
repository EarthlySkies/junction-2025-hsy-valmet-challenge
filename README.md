The Tuncklers' Junction 2025 HSY & Valmet Project
=================================================

The Tunckler's challenge response for Junction 2025: Utopia & Dystopia

The goal
--------

Optimize a given water pumping station to operate at minumum cost (based on
electricity prices), while staying within compliance and safety regulations.

The what
--------

Our program outputs 1 hour plans, split up into four 15 minute splits. These plans
dictate which pumps are running at what power and when.

The how
-------

We use a multi-agent system to keep track of conflicting variables which decide
when to pump the water at the most optimum times. We also have safety compliance
workers to keep track that the operation says within pre-defined safe operating
margings.

The problems
------------

### The Simulation ###

The simulation server reads data from the provide HSY files, which are static.
As such, the decisions our program makes have no effect on the provided data.
This leads to **all simulated decisions to be independent of each other.** As our
program cannot affect the input values it gets, the data we're receiving is essentially
random from the program's point of view.

E.g. if our program would recommend pumping a lot of water at a given time, yet
in the data HSY pumped only a little water, the next point in time we will still
have a high water level in the simulation, even if we would have lowered it in reality.

We simply did not have time to make a fully closed-loop simulation in where our
pumping would affect the actual L1 water level in a realistic way.

### The time ###

Our team simply didn't have enough time to polish and develop the program as much
as we would have liked to.
