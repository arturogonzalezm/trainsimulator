import datetime
import unittest
from unittest.mock import patch
from trainsimulator.exception import InvalidTimeFormat, InvalidTimeTable
from nose_parameterized import parameterized
from trainsimulator.model import TrainNetwork, Journey


class TestTrainNetwork(unittest.TestCase):
    @parameterized.expand([
        ([('a', 'c', None), ('a', 'b', None), ('b', 'd', None), ('d', 'e', None), ('b', 'e', None)],
         ('a', 'b', 'c', 'd', 'e'),
         (['b', 'c'], ['d', 'e'], None, ['e'], None)
         )
    ]
    )
    def test_find_next_station(self, network_nodes, start_stations, next_stations):
        train_network = TrainNetwork()
        train_network.build_network_from_nodes(network_nodes)
        for start_station_index, start_station in enumerate(start_stations):
            next_station = train_network._find_next_station(start_station)
            if next_station:
                self.assertCountEqual(next_station, next_stations[start_station_index])
            else:
                self.assertIsNone(next_station)

    @parameterized.expand([
        (
                [
                    ('a', 'c', None), ('a', 'b', None),
                    ('b', 'd', None), ('d', 'e', None),
                    ('b', 'e', None), ('e', 'f', None),
                    ('c', 'd', None), ('d', 'b', None), ('b', 'c', None)
                ],
                ('a', 'e'),

                [
                    ['a', 'c', 'd', 'e'],
                    ['a', 'c', 'd', 'b', 'e'],
                    ['a', 'b', 'd', 'e'],
                    ['a', 'b', 'e'],
                    ['a', 'b', 'c', 'd', 'e']
                ]
        ),
        (
                [
                    ('a', 'c', None), ('a', 'b', None),
                    ('b', 'd', None), ('d', 'e', None),
                    ('b', 'e', None)
                ],
                ('a', 'e'),

                [
                    ['a', 'b', 'd', 'e'],
                    ['a', 'b', 'e'],
                ]

        )
    ])
    def test_all_available_path(self, network_nodes, start_to_end, test_result):
        train_network = TrainNetwork()
        mocked_object = 'trainsimulator.model.Journey._uniform_time_format'
        with patch(mocked_object) as mocked_uniformat:
            mocked_uniformat.return_value = None
            train_network.build_network_from_nodes(network_nodes)
            start_station, end_station = start_to_end
            all_paths = train_network.all_valid_journey(start_station, end_station)
            self.assertCountEqual(all_paths, test_result)

    # @parameterized.expand([
    #     (
    #             [
    #                 {
    #                     '07:00': '09:00', '07:50': '09:50', '09:35': '11:35', '11:00': '13:00',
    #                 },
    #                 {
    #                     '06:15': '10:15', '07:15': '11:15', '08:30': '12:30', '10:30': '14:30', '11:00': '15:30'
    #                 },
    #                 {
    #                     '06:15': '10:15', '07:15': '11:15', '08:30': '12:30', '10:30': '14:30',
    #                 }
    #             ],
    #             '26:25'
    #     ),
    #     (
    #         [
    #             {'13:35': '21:42'},
    #             {'09:00': '09:50', '10:00': '10:50', '11:00': '11:50'}
    #         ],
    #         '20:15'
    #     ),
    # ])
    # def test__shortest_time_span(self, time_table, result):
    #     train_network = TrainNetwork()
    #     test_result = train_network._shortest_time_span(time_table)
    #     self.assertCountEqual(test_result, result)

    @parameterized.expand([
        ('1:04', '11:00', True),
        (datetime.datetime.strptime('13:05', '%H:%M'), datetime.datetime.strptime('15:05', '%H:%M'), True),
        ('23:04', '00:00', False),
        ('23:04', '0:0', False)
    ])
    def test_arrival_time_before_departure_time(self, arrival_time, departure_time, result):
        trainnetwork = TrainNetwork()
        test_result = trainnetwork._arrival_time_before_departure_time(arrival_time, departure_time)
        self.assertEqual(test_result, result)

    # @parameterized.expand([
    #     (['1:04', '8:00', '23:00'],
    #      ['8:00', '9:00', '10:00', '10:30', '11:30', '12:30', '12:55', '13:30', '15:30', '18:30', '23:00'],
    #      ['08:00', '09:00', '08:00']
    #      ),
    # ])
    # def test_earliest_departure_time(self, arrival_time, next_departure_time_table, result):
    #     trainnetwork = TrainNetwork()
    #     nodes = [('B', 'D', {'departure_time': next_departure_time_table, 'duration': '01:34'}), ('A', 'B', None)]
    #     trainnetwork.build_network_from_nodes(nodes)
    #     for index, arrival_time_each in enumerate(arrival_time):
    #         test_result = trainnetwork._earliest_departure_time(arrival_time_each, 'B')
    #         self.assertEqual(test_result, datetime.datetime.strptime(result[index], '%H:%M'))


    def test_departure_arrival_time_table(self):
        A_B = ['8:00', '9:00', '10:00', '10:30', '11:30', '12:30', '12:55', '13:30', '15:30', '18:30', '23:00']
        A_C = ['8:20', '9:20', '10:20', '10:38', '11:00', '12:15', '12:45', '13:00', '15:10', '19:30', '23:06']
        nodes = [('A', 'B', {'departure_time': A_B, 'duration': '01:34'}),
                 ('A', 'C', {'departure_time': A_C, 'duration': '02:05'})]
        trainnetwork = TrainNetwork()
        trainnetwork.build_network_from_nodes(nodes)
        time_table = trainnetwork._departure_arrival_time_table('A', 'C')
        A_C_departure_arrival_timetable = [
            ('08:20', '10:25'),
            ('09:20', '11:25'),
            ('10:20', '12:25'),
            ('10:38', '12:43'),
            ('11:00', '13:05'),
            ('12:15', '14:20'),
            ('12:45', '14:50'),
            ('13:00', '15:05'),
            ('15:10', '17:15'),
            ('19:30', '21:35'),
            ('23:06', '01:11')
        ]
        self.assertEqual(time_table, A_C_departure_arrival_timetable)

    # @parameterized.expand([
    #     (['19:23', '00:00', '23:50', '9:00'],
    #      {'9:00': '11:00', '10:00': '12:00', '15:00': '17:00', '18:00': '20:00', '23:50': '1:50', '00:30': '1:50'},
    #      ['23:50', '00:30', '00:30', '10:00'])
    # ])
    # def test_earlist_departure_time(self, arrival_time_list, departure_timetable, results):
    #     trainnetwork = TrainNetwork()
    #     for index, arrival_time in enumerate(arrival_time_list):
    #         test_result = trainnetwork._earliest_departure_time(arrival_time, departure_timetable)
    #         self.assertEqual(test_result, results[index])

    @parameterized.expand([
        (
                [
                    ('A', 'C', {'departure_time': ['09:00'], 'duration': '5:0'}),
                    ('A', 'B', {'departure_time': ['13:35'], 'duration': '8:07'}),
                    ('B', 'D', {'departure_time': ['20:07'], 'duration': '10:05'}),
                    ('D', 'E', {'departure_time': ['19:02'], 'duration': '2:3'}),
                    ('B', 'E', {'departure_time': ['9:00', '10:00', '11:00'], 'duration': '00:50'})
                ],
                ['A', 'B', 'E'],
                [{'13:35': '21:42'}, {'09:00': '09:50', '10:00': '10:50', '11:00': '11:50'}]
        ),
    ])
    def test_time_table_from_route(self, nodes, route, result):
        trainnetwork = TrainNetwork()
        trainnetwork.build_network_from_nodes(nodes)
        test_result = trainnetwork._time_table_from_route(route)
        self.assertCountEqual(test_result, result)
        trainnetwork.shortest_route('A', 'E')

    @parameterized.expand([
        (
                ['07:00', '10:00', '22:00', '00:10', '01:10'],
                ['1:00', '1:00', '1:00', '1:00'],
                ['08:00', '11:00', '23:00', '01:00'],
                '18:10'
        ),

        (
                ['10:00', '10:00', '10:00', '20:00'],
                ['10:0', '10:0', '10:0'],
                ['20:00', '20:00', '20:00'],
                '58:0'
        ),
        (
                ['10:00', '10:00', '10:00', '16:00'],
                ['30:0', '30:0', '30:0'],
                ['16:00', '16:00', '16:00'],
                '126:0'
        ),
    ])
    def test_time_span(self, time_sequence, duration, arrival_time, result):
        trainnetwork = TrainNetwork()
        test_result = trainnetwork._time_span(time_sequence, duration, arrival_time)
        self.assertEqual(test_result, result)


class TestJourney(unittest.TestCase):
    @parameterized.expand([
        (
                ['09:04', '12:05', '22:34', '23:59', '00:00'],
                '1:03',
                ['10:07', '13:08', '23:37', '01:02', '01:03']
        ),
        (
                ['09:04', '12:05', '22:34', '23:59', '00:00'],
                '25:03',
                ['10:07', '13:08', '23:37', '01:02', '01:03']
        ),
        (
                ['09:04', '12:05', '22:34', '23:59', '00:00'],
                '49:03',
                ['10:07', '13:08', '23:37', '01:02', '01:03']
        ),

    ])
    def test_arrival_time(self, departure_time, duration, arrival_time):

        time_table = {'departure_time': departure_time, 'duration': duration}
        journey = Journey('A', 'E')
        journey.timetable = time_table
        for index, every_departure_time in enumerate(departure_time):
            test_arrival_time = journey.arrival_time(every_departure_time)
            self.assertEqual(test_arrival_time, datetime.datetime.strptime(arrival_time[index], '%H:%M'))

    @parameterized.expand([
        ('01:02', '01:02'),
        ('1:02', '01:02'),
        ('01:2', '01:02'),
        ('1:2', '01:02')
    ])
    def test_uniform_time_format(self, time_str, result):
        journey = Journey('A', 'B')
        test_result = journey._uniform_time_format(time_str)
        self.assertEqual(test_result, result)

    @parameterized.expand([
        ({}, {'error': InvalidTimeTable}),
        ({'departuer_time': ['20:00']}, {'error': InvalidTimeTable}),
        ({'duration': '20:03'}, {'error': InvalidTimeTable}),
        ({'departuer_time': ['20:00']}, {'error': InvalidTimeTable}),
        ({'duration': '20:03'}, {'error': InvalidTimeTable}),
        ({'departuer_time': ['20:00'], 'duration': ''}, {'error': InvalidTimeTable}),
        ({'departuer_time': None, 'duration': '1:05'}, {'error': InvalidTimeTable}),
        ({'departure_time': ['20:00', '01:04', '23:12'], 'duration': '1:05'},
         {'departure_time': ['20:00', '01:04', '23:12'], 'duration': '1:05'}),
        ({'departure_time': ['5:00', '1:04', '23:12'], 'duration': '1:05'},
         {'departure_time': ['05:00', '01:04', '23:12'], 'duration': '1:05'}),
        ({'departure_time': [datetime.datetime.strptime('20:00', '%H:%M')], 'duration': '01:04'},
         {'error': InvalidTimeFormat}),

    ])
    def test_uniformat_timetable(self, timetable, result):
        journey = Journey('A', 'B')
        if 'error' in result:
            with self.assertRaises(result['error']):
                journey._uniformat_timetable(timetable)
        else:
            test_result = journey._uniformat_timetable(timetable)
            self.assertEqual(test_result, result)


if __name__ == '__main__':
    unittest.main()
