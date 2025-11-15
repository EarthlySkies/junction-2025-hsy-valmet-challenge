from fastapi import FastAPI
from fastapi.responses import PlainTextResponse
import uvicorn
from pydantic import BaseModel


#todo
#add data from dataset later (make the values in scenarios copy it more)
#add constant inflow (from data)

water_level = 2.0

max_water_level = 7.5
scenario_to_use = 0



## Parse the data from csv
import pandas as pd

csv_file = "Hackathon_HSY_data.csv"

# Read CSV
df = pd.read_csv(csv_file)

# Get last column name
last_col = df.columns[-1]

# Row 3 in Excel-style indexing = index 2 in pandas
start_index = 2
count = 96
end_index = start_index + count  # non-inclusive

# Slice and convert to list
values = df[last_col].iloc[start_index:end_index].tolist()

### Eletricity scenarios
elec = [
values
]

print(elec)
# [
# 	0.21, 1.36, 0.1, 2.4, 0.1, 
#  	0.1, 0.16, 0.1, 0.97, 0.1, 
#  	0.1, 0.1, 0.1, 1.72, 2.63, 
#  	1.87, 0.1, 0.1, 2.56, 1.77, 
#  	0.96, 3.43, 4.82, 2.1, 4.3, 
#  	2.98, 3.23, 1.81, 2.42, 4.09,
# 	2.41, 3.03, 4.93, 0.94, 0.1, 
# 	2.4, 0.77, 0.1, 0.1, 1.88, 0.1,
# 	1.23, 0.63, 0.1, 1.13, 0.6, 0.1,
# 	0.1, 0.1, 1.62, 0.1, 0.1, 0.1, 0.1,
# 	2.67, 3.79, 3.57, 5.21, 2.15, 0.87,
# 	0.1, 0.1, 1.21, 1.24, 2.3, 2.73,
# 	3.13, 3.19, 4.22, 1.96, 0.84, 
# 	0.17, 0.1, 2.67, 4.44, 2.72, 
# 	3.18, 2.56, 0.18, 0.1, 0.1, 2.19,
# 	1.14, 2.81, 1.76, 0.65, 2.43, 2.56, 
# 	0.1, 0.1, 0.11, 0.1, 0.1, 1.58, 0.1, 0.1]



### Normal dry inflow scenarios
dry_inflow = [
[
    1.15, 0.9399999999999999, 0.79, 0.89,
    1.02, 0.92, 0.97, 0.85,
    1.1, 1.11, 0.97, 1, 0.84,
    0.5600000000000001, 0.5,
    0.74, 0.93, 1.11, 0.91, 0.95,
    1.29, 0.96, 0.78, 0.79, 0.71,
    0.78, 1.1, 1.1, 0.75, 0.62,
    0.99, 0.89, 0.9399999999999999,
    0.98, 1.07, 0.89, 0.91, 0.58,
    0.5, 0.5, 0.9, 0.71,
    0.5, 0.71, 0.6,
    0.5600000000000001,
    0.96, 1.14, 1.43,
    1.67, 1.43, 1.65,
    1.74, 1.46, 1.59,
		1.34, 1.24, 1.08,
    1.23, 1.48, 1.62,
		1.79, 1.82, 1.66,
		1.58, 1.36, 1.53,
    1.39, 1.06, 1.28,
    1.02, 0.95, 1.11,
    0.86, 1.1, 1.32,
    1.32, 1.0, 0.8100000000000001,
    0.79, 0.91,0.88,
    0.71, 0.62, 0.5,
    0.5, 0.9, 0.58,
    0.72, 0.96, 1.16,
    0.79, 0.78, 0.85,
    1.03, 0.6899999999999999
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
		
	water_level = water_level + (dry_inflow[scenario_to_use][CURRENT_TICK]) - (CURRENT_ADDITIONAL_OUTFLOW)
		
	if(water_level > max_water_level):
		LOST = True

	if CURRENT_TICK < (len(dry_inflow[scenario_to_use]) - 1):
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

@app.get("/next-dry_inflow", response_class=PlainTextResponse)
async def incoming_dry_inflow():
	if CURRENT_TICK + 1 == len(dry_inflow[scenario_to_use]):
		return str(dry_inflow[scenario_to_use][0])
	else:
		return str(dry_inflow[scenario_to_use][CURRENT_TICK+1])

if __name__ == "__main__":
	# Run using the app object directly to ensure startup events run
	uvicorn.run(app, host="127.0.0.1", port=8000)