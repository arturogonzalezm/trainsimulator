import os
import sys
import datetime
from trainsimulator.constants import ROUTES
from trainsimulator.util import verify_departure_time, verify_duration
from trainsimulator.model import Journey, TrainNetwork

sys.path.append(os.path.join(os.path.dirname(__file__), '/trainsimulator/'))


def run():
    print('*' * 10 + 'Initialising Train Network' + '*' * 10)
    routes = []
    for route in ROUTES:
        route_timetable = {}
        start_station, end_station = route.split('-')
        print('{decoration}{route}:'.format(route=route, decoration='*' * 5))
        input_ = {
            'departure_time': verify_departure_time,
            'duration': verify_duration
        }
        for type_of_input, verify_method in input_.items():
            valid_input = False
            while not valid_input:
                if type_of_input == 'departure_time':
                    print("Please provide departure time with format 'hour:minute' for route {}, "
                          "separated by space, e.g 12:00, 15:32".format(route))
                else:
                    print("Please provide length of this route with format 'hour:minute', only one duration only")
                output = input('->')
                if not verify_method(output):
                    print('{} format is illegal, please try again, '.format(type_of_input))
                else:
                    if type_of_input == 'departure_time':
                        output = [i for i in output.split() if i.strip() != '']
                    else:
                        output = output.strip()

                    route_timetable[type_of_input] = output
                    valid_input = True

        journey = Journey(start_station, end_station)
        journey.timetable = route_timetable
        routes.append(journey)

    start_time = datetime.datetime.now()
    train_network = TrainNetwork()
    train_network.build_network_from_journey(routes)
    shortest_time = train_network.shortest_route('A', 'E')
    finish_time = datetime.datetime.now()
    if not shortest_time:
        print('no journey available from A to E, please check timetable is correct')
    else:
        print('The quickest route is {route}, duration {duration}'.
              format(route=shortest_time[0], duration=shortest_time[1]))

    print(finish_time - start_time)


if __name__ == '__main__':
    run()
