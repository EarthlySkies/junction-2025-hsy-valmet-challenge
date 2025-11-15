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

## This component can override the desires of the agents, as L1 simply **must**
## be emptied, even if the agents don't necessarily believe it to be efficient.

#from rain_tracker_agent import rain_tracker_agent
from datetime import datetime
from openpyxl import load_workbook

EXCEL_FILE_PATH = 'Hackathon_HSY_data.xlsx'
DATE_COLUMN_INDEX = 1  # Column A: "Time stamp"
#PRICE1_COLUMN_INDEX = 30  # Column AD: "High price"
PRICE2_COLUMN_INDEX = 31 # Column AE: "Normal price"

NEW_DATE_FORMAT = "%d/%m/%y %I:%M:%S %p"

# --- 1. Data Extraction from XLSX ---
def excel_to_tuple(PRICE_COLUMN_INDEX):
    price_list = []
    time_list = []
    try:
        workbook = load_workbook(filename=EXCEL_FILE_PATH, read_only=True)
        sheet = workbook.active
        for row in sheet.iter_rows(min_row=3):
            dt_object = row[DATE_COLUMN_INDEX - 1].value
            price_value = row[PRICE_COLUMN_INDEX - 1].value
            if isinstance(dt_object, datetime) and price_value is not None:
                time_list.append((dt_object, float(price_value)))
        #print(f"✅ Successfully extracted {len(time_list)} records from XLSX.")

    except FileNotFoundError:
        print(f"❌ Error: File not found at '{EXCEL_FILE_PATH}'. Ensure the path is correct.")
    except Exception as e:
        print(f"❌ An error occurred during XLSX processing: {e}")

    # --- 2. Conversion of Example Data ---
    for date_str, value in zip(time_list, price_list):
        try:
            dt_object = datetime.strptime(date_str, NEW_DATE_FORMAT)
            time_list.append((dt_object, value))
        except ValueError as e:
            print(f"Error parsing date string '{date_str}': {e}")
    return time_list

def adays_data(price_list):
    first_day = price_list[0][0].day
    todays_prices = []
    i = 0
    for hour_min, price in price_list:
        todays_prices.append((hour_min, price))
        if hour_min.day != first_day:
            break
        i += 1
    second_day = price_list[i][0].day
    for hour_min, price in price_list[i:]:
        todays_prices.append((hour_min, price))
        if hour_min.day != second_day:
            break
    todays_prices.pop()   # remove first element from next day
    return todays_prices


def optimal_time_to_empty(price_list):
    hourly_prices = adays_data(price_list)
    window_size = 8
    best_sum = float('inf')
    best_start = None
    for i in range(len(hourly_prices) - window_size + 1):
        window = hourly_prices[i:i + window_size]
        price_sum = sum(price for _, price in window)
        if price_sum < best_sum:
            best_sum = price_sum
            best_start = i

    return (hourly_prices[best_start], hourly_prices[best_start + window_size - 1])

def optimal_tunnelwindow():
    #price1_list = excel_to_tuple(PRICE1_COLUMN_INDEX)
    price2_list = excel_to_tuple(PRICE2_COLUMN_INDEX)

    #precipitation = rain_tracker_agent()
    #bestime_high = optimal_time_to_empty(price1_list)
    bestime = optimal_time_to_empty(price2_list) # tuple( datetime(YY,MM,DD,hh,mm), price)
    return bestime

optimal_tunnelwindow()
