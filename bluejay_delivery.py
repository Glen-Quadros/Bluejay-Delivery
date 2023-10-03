import pandas as pd
import numpy as np

def has_worked_consec_days(employee_data):
    schedule_dates = employee_data['Time'].dt.date
    consecutive_days = 0
    for i in range(len(schedule_dates) - 1):
        if (schedule_dates.iloc[i + 1] - schedule_dates.iloc[i]).days == 1:
            consecutive_days += 1
            if consecutive_days == 7:
                return True
        else:
            consecutive_days = 0
    return False

def convert_to_timedelta(time_str):
    if isinstance(time_str, str):
        hours, minutes = map(int, time_str.split(':'))
        return pd.Timedelta(hours=hours, minutes=minutes)
    return pd.Timedelta(hours=0)

def has_short_breaks(employee_data):
    shift_start_times = employee_data['Time']
    for i in range(len(shift_start_times) - 1):
        time_diff = (shift_start_times.iloc[i + 1] - shift_start_times.iloc[i])
        if pd.Timedelta(hours=1) < time_diff < pd.Timedelta(hours=10):
            return True
    return False

def has_long_shift(employee_data):
    shift_durations = employee_data['Timecard Hours (as Time)'].apply(convert_to_timedelta)
    for duration in shift_durations:
        if duration.total_seconds() > 14 * 3600:
            return True
    return False

def main():
    df = pd.read_excel('/content/Assignment_Timecard.xlsx')

    with open('output.txt', 'w') as output_file:
        for name, employee_data in df.groupby('Employee Name'):
            if has_worked_consec_days(employee_data):
                output_file.write(f"{name} has worked for 7 consecutive days.\n")
            if has_short_breaks(employee_data):
                output_file.write(f"{name} has short breaks between shifts.\n")
            if has_long_shift(employee_data):
                output_file.write(f"{name} has worked for more than 14 hours in a single shift.\n")

if __name__ == "__main__":
    main()

