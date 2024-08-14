import csv
from collections import defaultdict
from datetime import datetime
from calendar import month_name

def process_energy_data(file_path):
    monthly_consumption = defaultdict(float)
    days_count = defaultdict(int)
    daily_averages = []
    date_format = "%d.%m.%Y"

    first_date = None
    last_date = None

    with open(file_path, 'r', encoding='utf-8-sig') as file:
        reader = csv.reader(file, delimiter=';')

        # Skip the header row
        next(reader, None)

        for row in reader:
            if len(row) < 2:
                continue  # Skip lines that don't have enough columns
            date_str, consumption_str = row[0], row[1]
            try:
                # Convert date and consumption values
                date = datetime.strptime(date_str, date_format)
                consumption = float(consumption_str.replace(',', '.'))
                
                # Use the year and month as the key for monthly consumption
                month_key = (date.year, date.month)
                monthly_consumption[month_key] += consumption
                days_count[month_key] += 1

                # Track the first and last date
                if first_date is None or date < first_date:
                    first_date = date
                if last_date is None or date > last_date:
                    last_date = date
            except ValueError:
                # Handle any errors in data conversion
                print(f"Error processing row: {row}")

    # Calculate daily averages for each month
    for (year, month), consumption in monthly_consumption.items():
        if days_count[(year, month)] > 0:
            daily_average = consumption / days_count[(year, month)]
            daily_averages.append(daily_average)

    # Calculate the overall average of daily averages
    if daily_averages:
        overall_daily_average = sum(daily_averages) / len(daily_averages)
    else:
        overall_daily_average = 0

    # Calculate total energy consumption in the period
    total_consumption = sum(monthly_consumption.values())
    
    # Calculate average consumption per month
    month_count = len(monthly_consumption)
    if month_count == 0:
        print("No valid data found.")
        return

    average_consumption = total_consumption / month_count

    # Print results in a table-like format
    print(f"{'Year-Month':<20} {'Total Consumption (kWh)':<30} {'Daily Average (kWh/day)':<30}")
    print("-" * 75)

    for (year, month), consumption in sorted(monthly_consumption.items()):
        daily_average = consumption / days_count[(year, month)]
        month_name_str = month_name[month]
        print(f"{year} - {month_name_str:<10} {consumption:>25.2f} {daily_average:>25.2f}")

    print("-" * 75)
    print(f"\nTotal energy consumption in the period: {total_consumption:.2f} kWh")
    print(f"Average monthly consumption = {average_consumption:.2f} kWh")
    print(f"Overall daily average of monthly daily averages = {overall_daily_average:.2f} kWh/day")

# Path to your data file
file_path = 'energy_data.csv'
process_energy_data(file_path)
