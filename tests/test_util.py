import unittest
import datetime
from nose_parameterized import parameterized
from trainsimulator.util import (
    rearrange_dict, earliest_time,
    time_span, verify_time_format, verify_duration,
    verify_departure_time)


class TestUtilFunc(unittest.TestCase):
    @parameterized.expand([
        (
                {'a': [1, 2, 3], 'b': 4},
                [('a', 1), ('a', 2), ('a', 3), ('b', 4)]
        )
    ])
    def test_rearrange_dict(self, input_dict, result):
        test_result = rearrange_dict(input_dict)
        self.assertCountEqual(test_result, result)

    @parameterized.expand([
        (
                ['15:05', '10:00', '7:00', '7:45', '22:32'],
                '07:00'
        ),
        (
                [datetime.datetime.strptime('23:05', '%H:%M'), '12:07', '11:53', '4:02',
                 datetime.datetime.strptime('14:37', '%H:%M')],
                '04:02'
        )
    ])
    def test_earliest_time(self, time_sequence, result):
        test_result = earliest_time(time_sequence)
        self.assertEqual(test_result, result)

    @parameterized.expand([
        (
                ['7:00', '10:00', '22:00', '00:10', '01:45'],
                '18:45'
        ),
        (
                [datetime.datetime.strptime('4:05', '%H:%M'),
                 '11:07', '12:53', '23:02',
                 datetime.datetime.strptime('00:37', '%H:%M')],
                '20:32'
        ),
        (
                ['2:00', '4:00'],
                '2:0'
        ),
        (
                ['7:00', '10:30', '6:15', '10:15'],
                '27:15'
        ),
        (
                ['9:00', '9:15'],
                '0:15'
        ),
        (
                ['09:35', '06:15', '10:30', '14:30'],
                '28:55'
        ),
        (
                ['11:00', '06:15', '10:30', '14:30'],
                '27:30'
        ),
        (
                ['07:50', '10:30', '06:15', '10:15'],
                '26:25'

        )

    ])
    def test_time_span(self, time_sequence, result):
        test_result = time_span(time_sequence)
        self.assertEqual(test_result, result)

    @parameterized.expand([
        ('02:32', True),
        ('ab:01', False),
        ('123:34', False),
        ('1:2', True),
        ('01:2', True),
        ('01:02', True),
        ('24:00', False),
        ('23:60', False),
        ('25:68', False)
    ])
    def test_verify_time_format(self, time_str, result):
        test_result = verify_time_format(time_str)
        self.assertEqual(test_result, result)

    @parameterized.expand([
        ('02:32', True),
        ('ab:01', False),
        ('123:34', True),
        ('1:2', True),
        ('01:2', True),
        ('01:02', True),
        ('12:45', True),
        ('2:60', False),
        ('22:00', True),
        ('28:00', True),
        ('28:69', False),
        ('0:0', False)
    ])
    def test_duration_time_format(self, time_str, result):
        test_result = verify_duration(time_str)
        self.assertEqual(test_result, result)

    @parameterized.expand([
        ('02:32 ab:01 123:34 1:2 01:2', False),
        ('01:02 12:45 2:60 22:00 28:00 28:69', False),
        ('9:05 10:15 12:07 22:08 00:00', True),
        ('9:05 10:15 12:07 22:08 00:00', True),
        (' 9:05    10:15 12:07 22:08    00:00  \n', True),
        ('00:01', True)

    ])
    def test_verify_departure_time(self, time_str, result):
        test_result = verify_departure_time(time_str)
        self.assertEqual(test_result, result)


if __name__ == "__main__":
    unittest.main()
