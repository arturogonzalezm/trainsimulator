import unittest
import datetime
from nose_parameterized import parameterized
from trainsimulator.util import (
    verify_time_format, verify_duration,
    verify_departure_time)


class TestUtilFunc(unittest.TestCase):

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
