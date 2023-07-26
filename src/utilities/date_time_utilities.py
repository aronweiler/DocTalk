from datetime import datetime, date
import pytz
from tzlocal import get_localzone

def get_local_time_offset(input_date):
    # Get the local time zone for the region you are running Windows in
    local_tz = get_localzone()

    # Get the time zone offset for the specific date
    offset = local_tz.utcoffset(datetime.combine(input_date, datetime.min.time()))

    # Convert the offset to the format '-HH:MM'
    offset_hours = offset.total_seconds() // 3600
    offset_minutes = (offset.total_seconds() % 3600) // 60
    offset_str = f"{int(offset_hours):+03d}:{int(offset_minutes):02d}"

    return offset_str

def generate_time_string(input_date):
    # Get the current local time zone offset
    offset_str = get_local_time_offset(input_date)

    # Combine the input date with the time 00:00:00 to create a datetime object
    input_datetime = datetime.combine(input_date, datetime.min.time())

    # Get the current datetime in the local time zone
    local_datetime = input_datetime.astimezone(pytz.utc).astimezone()

    # Format the datetime as a string with the local time zone offset
    time_string = local_datetime.strftime(f"%Y-%m-%dT%H:%M:%S{offset_str}")

    return time_string

if __name__ == "__main__":
    # Example usage: Generate the time string for the date '2023-07-25'
    input_date = date(2023, 7, 25)
    result_time_string = generate_time_string(input_date)
    print("Time String with Local Time Zone Offset:", result_time_string)
