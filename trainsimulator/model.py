import datetime
from collections import defaultdict
from trainsimulator.util import sort_time, verify_time_format, convert_to_datetime, convert_to_timedelta
from trainsimulator.exception import (
    InvalidTimeTable, InvalidNetwork, InvalidStation, NoTimetableAvailable, InvalidTimeFormat)


def time_span_decorator(func):
    def wrapper(*args):
        time_sequence = args[1]
        duration = args[2]
        arrival_time = args[3]
        time_sequence = convert_to_datetime(time_sequence)
        duration = convert_to_timedelta(duration)
        arrival_time = convert_to_datetime(arrival_time)

        return func(args[0], time_sequence, duration, arrival_time)

    return wrapper


class Journey(object):
    """
    self._timetable is a dictionary in the format of departure_time: [duration]
    """

    def __init__(self, start_station, end_station):
        self._start_station = start_station
        self._end_station = end_station
        self._timetable = {}
        self._departure_time = None

    @property
    def timetable(self):
        return self._timetable

    @timetable.setter
    def timetable(self, time_table):
        self._timetable = self._uniformat_timetable(time_table)

    @property
    def duration(self):
        return self.timetable['duration']

    def update_timetable(self, departure_time, duration):

        if departure_time:
            self._timetable['departure_time'] = departure_time
        if duration:
            self._timetable[duration] = duration

    @property
    def start_station(self):
        return self._start_station

    @property
    def end_station(self):
        return self._end_station

    @property
    def departure_time(self):
        if self._departure_time is None:
            self._departure_time = self._extract_departure_time()

        return self._departure_time

    def arrival_time(self, departure_time):
        if departure_time not in self.timetable.get('departure_time'):
            return
        duration = self.timetable['duration']
        departure_time_stamp = datetime.datetime.strptime(departure_time, '%H:%M')
        duration_hour, duration_min = duration.split(':')
        duration_time_stamp = datetime.timedelta(hours=int(duration_hour), minutes=int(duration_min))
        arrival_time = (departure_time_stamp + duration_time_stamp).strftime('%H:%M')
        return datetime.datetime.strptime(arrival_time, '%H:%M')

    def _extract_departure_time(self):
        return self.timetable['departure_time']

    def departure_arrival_time_table(self):
        time_table = [(departure_time, self.arrival_time(departure_time).strftime('%H:%M'))
                      for departure_time in self.departure_time]
        return time_table

    def _uniform_time_format(self, time_str):
        if not time_str or not verify_time_format(time_str):
            return None

        hour, minute = time_str.split(':')
        new_format = ['0' + i if len(i) == 1 else i for i in [hour, minute]]
        return ':'.join(new_format)

    def _uniformat_timetable(self, time_table):
        sanitized_time_format = []
        if time_table.get('departure_time') and time_table.get('duration'):
            for time_stamp in time_table['departure_time']:
                if isinstance(time_stamp, str):
                    sanitized_time_ = self._uniform_time_format(time_stamp)
                    if sanitized_time_:
                        sanitized_time_format.append(sanitized_time_)
                    else:
                        raise InvalidTimeFormat
                else:
                    raise InvalidTimeFormat
            time_table['departure_time'] = sanitized_time_format
            return time_table
        else:
            raise InvalidTimeTable


class TrainNetwork(object):
    def __init__(self):
        """
        self.journey = {'start_station': journey_instance}
        """
        self.journey = defaultdict(list)
        self.all_station = set()

    def _journey_instance(self, start_station):
        if start_station not in self.journey:
            return

        return self.journey[start_station]

    def journey_duration(self, start_station, end_station):
        journey_instance = [i for i in self._journey_instance(start_station) if i.end_station == end_station]
        return journey_instance[0].duration if journey_instance else None

    def build_network_from_nodes(self, nodes):
        try:
            if not nodes:
                raise ValueError

            self.all_station = set()
            for node in nodes:
                start_station, end_station, time_table = node
                journey = Journey(start_station, end_station)
                if time_table:
                    journey.timetable = time_table
                self.journey[start_station].append(journey)
                self.all_station.update({start_station, end_station})
        except (ValueError, InvalidTimeTable):
            print('Invalid nodes, quit')
            raise InvalidNetwork

    def build_network_from_journey(self, journeys):
        self.all_station = set()

        for journey in journeys:
            self.journey[journey.start_station].append(journey)
            self.all_station.update({journey.start_station, journey.end_station})

    def _find_next_station(self, start_station):
        if start_station not in self.journey:
            return
        journey_instances = self.journey[start_station]

        end_stations = [journey_instance.end_station for journey_instance in journey_instances]
        return end_stations

    def _arrival_time_before_departure_time(self, arrival_time, departure_time):
        time_sequence = []
        for time_stamp in [arrival_time, departure_time]:
            if isinstance(time_stamp, str) and verify_time_format(time_stamp):
                time_sequence.append(datetime.datetime.strptime(time_stamp, '%H:%M'))
                continue

            if isinstance(time_stamp, datetime.datetime):
                time_sequence.append(time_stamp)

        if len(time_sequence) == 2:
            time_difference = time_sequence[0] - time_sequence[1]
            return time_difference < datetime.timedelta(minutes=0)
        else:
            raise InvalidTimeFormat

    def _is_departure_station(self, station_name):
        return station_name in self.journey

    def _find_available_paths(self, start_station, end_station, result, results):
        next_station = self._find_next_station(start_station)
        if not result or not next_station:
            return None

        for i in next_station:

            if i in result:
                continue
            if i == end_station:
                results.append(result + [i])
                continue
            result.append(i)
            temp_result = self._find_available_paths(i, end_station, result, results)
            if not temp_result:
                result.pop()
                continue
            result = temp_result
        return result[:-1]

    def all_valid_journey(self, start_station, end_station):
        """
        This method is to generate all the paths from start station to end station
        :param start_station: 
        :param end_station: 
        :return: 
        """
        if start_station not in self.all_station or end_station not in self.all_station:
            raise InvalidStation

        result = [start_station]
        results = []
        self._find_available_paths(start_station, end_station, result, results)
        return results

    def _departure_arrival_time_table(self, start_station, end_station):
        if start_station not in self.journey:
            return
        for journey in self.journey[start_station]:
            if journey.end_station == end_station:
                return journey.departure_arrival_time_table()

    def _time_table_from_route(self, route):
        """
        This method is to generate the timetable of the route
        :param route: 
        :return: 
        """
        trip_time_table = []
        for index, start_stop in enumerate(route[:-1]):
            next_stop = route[index + 1]

            time_table = self._departure_arrival_time_table(start_stop, next_stop)
            trip_time_table.append(dict(time_table))

        return trip_time_table

    def _earliest_departure_time(self, arrival_time, next_stop_timetable):
        earliest_departure_time_ = None
        next_stop_departure_time = sort_time(list(next_stop_timetable.keys()))
        for departure_time in next_stop_departure_time:
            if self._arrival_time_before_departure_time(arrival_time, departure_time):
                earliest_departure_time_ = departure_time
                break

        return earliest_departure_time_.strftime('%H:%M') if earliest_departure_time_ else next_stop_departure_time[
            0].strftime('%H:%M')

    @time_span_decorator
    def _time_span(self, time_sequence, duration, arrival_time):
        accumulated_time = datetime.timedelta(hours=0, minutes=0)
        last_index = len(time_sequence) - 2
        for index, time in enumerate(time_sequence[:-1]):
            if index == last_index:
                accumulated_time = accumulated_time + duration[index]
                break
            departure_time = time_sequence[index + 1]
            arrival_time_ = arrival_time[index]

            if arrival_time_ <= departure_time:
                time_interval = duration[index] + departure_time - arrival_time_
            else:
                time_interval = duration[index] + departure_time - arrival_time_ + datetime.timedelta(hours=24)

            accumulated_time = accumulated_time + time_interval

        if accumulated_time.days > 0:
            hour_, minutes, _ = str(accumulated_time).split(',')[1].strip().split(':')
            new_hours = int(hour_) + 24 * accumulated_time.days

            return ':'.join([str(new_hours), str(int(minutes))])

        hour_, minutes, _ = str(accumulated_time).split(':')

        return ':'.join([str(int(hour_)), str(int(minutes))])

    def _shortest_time_span(self, time_table, route):
        """
        This method is re-organize time table into time sequence
        :param time_table: 
        :return: 
        """
        result = []
        total_routes = len(time_table)
        duration = [self.journey_duration(station, route[i + 1]) for i, station in enumerate(route[:-1])]
        for first_departure_time, arrival_time in time_table[0].items():
            arrival_time_list = [arrival_time]
            available_departure_time = [first_departure_time]
            earliest_arrival_time = arrival_time
            for route_index, timetable in enumerate(time_table[1:], 1):

                earliest_departure_time = self._earliest_departure_time(earliest_arrival_time, timetable)
                earliest_arrival_time = timetable[earliest_departure_time]
                arrival_time_list.append(earliest_arrival_time)
                available_departure_time.append(earliest_departure_time)
                if route_index == total_routes - 1:
                    available_departure_time.append(earliest_arrival_time)
            result.append({'time_sequence': available_departure_time,
                           'duration': duration, 'arrival_time': arrival_time_list})
        time_consumed = [self._time_span(i['time_sequence'], i['duration'], i['arrival_time']) for i in result]
        return min(time_consumed)

    def shortest_route(self, start_station, end_station):
        all_paths = self.all_valid_journey(start_station, end_station)
        journey_len = {}
        for route in all_paths:
            time_table = self._time_table_from_route(route)
            if not time_table:
                continue
            shortest_time = self._shortest_time_span(time_table, route)
            journey_len[''.join(route)] = shortest_time

        if journey_len:
            quickest_path = min(journey_len, key=journey_len.get)
            return quickest_path, journey_len[quickest_path]
