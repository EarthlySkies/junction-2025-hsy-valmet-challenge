## This component ensures that the water storage reaches level L1 at least
## every two days for compliance reasons.

## L1 storage **must** be emptied to L1 min every 2 days. It can be emptied
## more frequently if desired, but minumum is every 48 hours.

## The job of this component is to figure out the optimum timing for emptying
## the storage tank to its minimum level. This is for compliance reasons, as
## the tank must be emptied to clean out soot at the bottom.

## This job cannot be skipped. Thus, it cannot be relegated to an agent, as
## it could lead to conditions where the other agents see no reason to empty
## the tanks. In such a case, the tank could never be emptied, breaching compliance.
## For that reason, this function to be in a separate, non-agent component.
