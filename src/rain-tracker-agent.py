## This agent tracks the amount of predicted rain
## Outputs more desire the more rain there is.
## Output is between 0.0 to +1.0
## Currently 1.0 is when the precipitation is 5 or higher 

import requests

def rain_tracker_agent(rain):
    # Clamp rain to [0, 5] range
    if rain < 0:
        rain = 0.0
    elif rain >= 5:
        return 1.0
    
    # Normalize linearly: 0 mm -> 0.0, 5 mm -> 1.0
    normalized = rain / 5.0
    
    return normalized

    # lat, lon = 60.2052, 24.6522

    # url = "https://api.open-meteo.com/v1/forecast"
    # params = {
    #     "latitude": lat,
    #     "longitude": lon,
    #     "minutely_15": ["precipitation"],
    #     "timezone": "Europe/Helsinki",
    #     "forecast_minutely_15": 2
    # }

    # r = requests.get(url, params=params)
    # r.raise_for_status()
    # forecast = r.json()

    # minutely = forecast["minutely_15"]
    # prec = minutely["precipitation"]

    # # next 15-min slot value
    # p = prec[1]

    # # clamp to [0, 100]
    # if p < 0:
    #     p = 0.0
    # elif p > 100:
    #     p = 100.0

    # # normalize: 0 mm -> 0.0, 100+ mm -> 1.0, linear in between
    # normalized = p / 100.0


#print(rain_tracker_agent())