import re
from datetime import datetime, timedelta
from trainsimulator.exception import InvalidTimeFormat


def convert_to_datetime(time_sequence):
    sanitized_time_sequence = []
    for time_stamp in time_sequence:
        if not isinstance(time_stamp, (str, datetime)):
            raise InvalidTimeFormat

        if isinstance(time_stamp, str):
            try:
                time_stamp = datetime.strptime(time_stamp, '%H:%M')

            except ValueError:
                raise InvalidTimeFormat
        sanitized_time_sequence.append(time_stamp)
    return sanitized_time_sequence


def convert_to_timedelta(time_delta):
    sanitized_time_sequence = []
    for timedelta_ in time_delta:
        if not isinstance(timedelta_, (str, timedelta)):
            raise InvalidTimeFormat

        if isinstance(timedelta_, str):
            try:
                hour, minute = timedelta_.split(':')
                timedelta_ = timedelta(hours=int(hour), minutes=int(minute))

            except ValueError:
                raise InvalidTimeFormat
        sanitized_time_sequence.append(timedelta_)
    return sanitized_time_sequence


def time_sequence_decorator(func):
    def wrapper(*args):
        time_sequence = args[0]
        if not time_sequence:
            return
        sanitized_time_sequence = convert_to_datetime(time_sequence)
        return func(sanitized_time_sequence)

    return wrapper


@time_sequence_decorator
def sort_time(time_sequence):
    return sorted(time_sequence)


def verify_time_format(time_str):
    if not isinstance(time_str, str):
        return False

    time_format = r'^(\d{1,2}):(\d{1,2})$'
    matched = re.match(time_format, time_str)
    if matched:
        if 0 <= int(matched.group(1)) < 24 and 0 <= int(matched.group(2)) < 60:
            return True
        else:
            print('Hour should be within [0, 24); Minute should be within [0, 60)')
            return False
    else:
        return False


def verify_duration(time_str):
    if not isinstance(time_str, str):
        return False
    time_format = r'^(\d.*):(\d{1,2})$'
    duration = re.match(time_format, time_str)
    if duration:
        minutes = int(duration.group(2))
        hour = int(duration.group(1))
        if 0 <= minutes < 60 and any([hour, minutes]):
            return True
        else:
            print('Minute should be within [0, 60)')
            return False
    else:
        print("Invalid format, should be '%H:%M' ")
        return False


def verify_departure_time(string):
    departure_time_list = [i for i in string.split() if i.strip != '']
    for departure_time in departure_time_list:
        if not verify_time_format(departure_time):
            return False
    return True
