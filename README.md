[![Build Status](https://travis-ci.org/arturosolutions/trainsimulator.svg?branch=master)](https://travis-ci.org/arturosolutions/trainsimulator)
[![Coverage Status](https://coveralls.io/repos/github/arturosolutions/trainsimulator/badge.svg?branch=master)](https://coveralls.io/github/arturosolutions/trainsimulator?branch=master)

# Train Simulation Python #

> ### Requirements:
1. Assume we live in city A and would like to travel to city E.
2. Assume there are only up to 5 cities - A, B, C, D, E.
3. Assume that you have some routes such as A connects to B, A connects to C, B connects to D, D connects to E, B connects to E.
4. Assume you are given a timetable of train departures (station A departure) and train route times (journey time to go from eg A to B).
5. Write a simulation which calculates the shortest time between city A and E and the route travelled using Python (2.7 or 3.X).
6. Design the structure of the input train timetable and journey lengths for the simulation.
7. Output the total time it takes to run and the route to the command line.
8. Make sure the routes are configurable for custom user input of timetables and journey lengths.
9. Ensure that this is production quality code including exception handling, unit tests etc. No third Party libraries to be used except in testing.

> ### Technical Specs:

- PyCharm or any editor/IDE that supports Python programming language
- Developed in Python 3.6
- The source code has been tested on MacOS and Linux and is compatible with Python 3.3 or later
- TDD and unit testing unittest
- Continuous Integration and testing Travis CI
- Version control GitHub
- Code coverage nosetests, coveralls, coverage

Third party libraries for testing purposes:

* nose_parameterized
* coverage
* coveralls
* tox

> ### Instructions:

1. Go inside your root directory.
2. Open your Terminal/command line/command prompt and type:
```commandline
python main.py
```
3. Follow the instructions by entering the requested values.

**Example:**

Inputs(can be one input 10:00 or several inputs separated by space 10:00 11:00):

```commandline
Please provide departure time with format 'hour:minute' for route A-B, separated by space, e.g 12:00, 15:32
->10:00
Please provide length of this route with format 'hour:minute', only one duration only
->1:30
*****A-C:
Please provide departure time with format 'hour:minute' for route A-C, separated by space, e.g 12:00, 15:32
->12:00
Please provide length of this route with format 'hour:minute', only one duration only
->1:30
*****B-D:
Please provide departure time with format 'hour:minute' for route B-D, separated by space, e.g 12:00, 15:32
->1:00
Please provide length of this route with format 'hour:minute', only one duration only
->00:30
*****D-E:
Please provide departure time with format 'hour:minute' for route D-E, separated by space, e.g 12:00, 15:32
->3:00
Please provide length of this route with format 'hour:minute', only one duration only
->1:00
*****B-E:
Please provide departure time with format 'hour:minute' for route B-E, separated by space, e.g 12:00, 15:32
->5:00
Please provide length of this route with format 'hour:minute', only one duration only
->2:00
The quickest route is ABDE, duration 18:0
0:00:00.014053
```

Output:
```commandline
The quickest route is ABDE duration 18:0
0:00:00.014053
```

> ### Tests:

* To see the results of the tests performed by Travis CI please refer to [test results](https://travis-ci.org/arturosolutions/trainsimulator)

* Please refer to [coverage results](https://coveralls.io/github/arturosolutions/trainsimulator?branch=master) to see the code coverage performed by coveralls

* nosetests and coverage results:
```commandline
Name                          Stmts   Miss Branch BrPart  Cover
---------------------------------------------------------------
trainsimulator.py                 0      0      0      0   100%
trainsimulator/exception.py      15      0      0      0   100%
trainsimulator/model.py         217     13     94      9    91%
trainsimulator/util.py           69      5     32      6    89%
---------------------------------------------------------------
TOTAL                           301     18    126     15    91%
----------------------------------------------------------------------
Ran 56 tests in 0.257s

OK
```
* unittest results:

![test_model](https://github.com/arturosolutions/trainsimulator/blob/master/docs/images/test_model.png)

![test_util](https://github.com/arturosolutions/trainsimulator/blob/master/docs/images/test_util.png)

* You can also run unittests with coverage and the results can be found inside docs/test_model and docs/test_util.

> ### Overview:

![diagram](https://github.com/arturosolutions/trainsimulator/blob/master/docs/images/diagram.png)

----

**Features:**

- The Train Network class is able to find all the possible combinations/routes between any two stations.
- It calculates the time between each station.
- Duration is configurable.
- Timetable is configurable.
- Journey length is configurable.

#

**Notes:**

* This program was written assuming the train speed is always the same.
* This program was written assuming the timetable is same everyday.
* This project is primarily part of a coding assessment.
* The command line is only using certain networks.

----

MIT License

Copyright (c) 2017 Arturo Gonzalez

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.