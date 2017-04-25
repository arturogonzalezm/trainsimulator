class InvalidTimeFormat(Exception):
    code = 7
    message = 'Invalid time format. Should be %H:%M'


class InvalidTimeTable(Exception):
    code = 10
    message = "Invalid time table. Should be {'departure_time': list of time str, 'duration': int}"


class InvalidNetwork(Exception):
    code = 15
    message = "Fail to build network."


class InvalidStation(Exception):
    code = 15
    message = "Station is not in the network."


class NoTimetableAvailable(Exception):
    code = 20
    message = "Couldn't extract a valid time table from the journey."
