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
- Python 3.3 onwards
- The source code has been tested on MacOS and Linux

Third party libraries:

- nose_parameterized 
- coverage

> ### Instructions:

1. Open your Terminal/command line/command prompt and type:
```commandline
python ~/.trainsimulation/examples/timetables_and_journey_lengths.py
```
2. Follow the instructions entering the values requested.

**Example:**

Inputs:

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


----

**Features:**

- The Train network class is able to find all the possible combinations/routes between any two stations.
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
