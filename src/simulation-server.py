from fastapi import FastAPI
from fastapi.responses import PlainTextResponse
import uvicorn
from pydantic import BaseModel

water_level = 2.0

max_water_level = 10
scenario_to_use = 0

### Rain scenarios - lets say the values can be only from 0 to 5
rain = [
[
	2, 3, 3, 3, 
	4, 5, 1, 0, 
	0, 3, 4, 4, 
	2, 4, 4, 5, 
	0, 0, 0, 0, 
	1, 1, 1, 1,
	3, 4, 5, 5,
	2, 1, 0, 0
]
]

### Eletricity scenarios
elec = [
[
	1, 1, 1, 5, 
	10, 15, 2, 2, 
	2, 1, 4, 4,
	4, 2, 2, 1,
	3, 4, 1, 2,
	4, 5, 6, 2,
	1, 1, 1, 2,
	2, 3, 2, 1
]
]

LOST = False
CURRENT_TICK = 0
CURRENT_ADDITIONAL_OUTFLOW = 0

### Game Loop
def GameLoop():
	
	global water_level
	global LOST
	global CURRENT_TICK
		
	water_level = water_level + (rain[scenario_to_use][CURRENT_TICK]) - (CURRENT_ADDITIONAL_OUTFLOW)
		
	if(water_level > max_water_level):
		LOST = True

	if CURRENT_TICK < (len(rain[scenario_to_use]) - 1):
		CURRENT_TICK = CURRENT_TICK + 1
	else:
		CURRENT_TICK = 0

app = FastAPI()

class OutflowRequest(BaseModel):
	outflow: float

@app.post("/outflow")
async def outflow(request: OutflowRequest):
	global CURRENT_ADDITIONAL_OUTFLOW
	CURRENT_ADDITIONAL_OUTFLOW = request.outflow
	
	GameLoop()

	print(water_level)
	return {"message": "15 minutes passed", "water_level": water_level}

@app.get("/water-level", response_class=PlainTextResponse)
async def water():
	if LOST == False:
		return str(water_level)
	else:
		return str(-1)

@app.get("/current-elec-price", response_class=PlainTextResponse)
async def elec_price():
	return str(elec[scenario_to_use][CURRENT_TICK])

@app.get("/all-upcoming-elec-price", response_class=PlainTextResponse)
async def all_upcoming_elec_price():
	return str(elec[scenario_to_use][CURRENT_TICK:])

@app.get("/next-rain", response_class=PlainTextResponse)
async def incoming_rain():
	if CURRENT_TICK + 1 == len(rain[scenario_to_use]):
		return str(rain[scenario_to_use][0])
	else:
		return str(rain[scenario_to_use][CURRENT_TICK+1])

if __name__ == "__main__":
	# Run using the app object directly to ensure startup events run
	uvicorn.run(app, host="127.0.0.1", port=8000)