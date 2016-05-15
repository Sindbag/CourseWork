# default file to read data from
FILENAME = 'input.txt'

# metric to be chosen
METRIC_NUMBER = 0
METRIC_POWER = 2

METRICS_LIST = [
    lambda x, y: float(pow(sum(abs(x.sensors[i] - y.sensors[i]) ** METRIC_POWER for i in range(len(x.sensors))),
                           1/METRIC_POWER)),
    lambda x, y: min([abs(x.sensors[i] - y.sensors[i]) for i in range(len(x.sensors))]),
    lambda x, y: max([abs(x.sensors[i] - y.sensors[i]) for i in range(len(x.sensors))])
]

# range to check sensors value to start Press
CHECK_FRAMES_RANGE = 10

# max sensors value to start Press
LOW_SENSOR_BORDER = 20

# max sensors value to stop Press
LOW_SENSOR_MISTAKE = 5

# count of SENSOR_INFO_SIZE to read by one attempt
DATA_CHUNK_SIZE = 300

# size of one sensor data reading (in lines)
SENSOR_INFO_SIZE = 7

# sensor's ideal shapes with name and ideal frames
SENSOR_CLASSES = [

    {
        'name': 'circle',
        'meta': 'SENSOR_CIRCLE',
        'centers_list': [

            [0, 0, 0,
             0, 255, 255, 0,
             0, 255, 0, 255, 0,
             0, 255, 255, 0,
             0, 0, 0],
        ]
    },

    {
        'name': 'line',
        'meta': 'SENSOR_LINE',
        'centers_list': [

            [0, 0, 0,
             0, 255, 0, 0,
             0, 0, 255, 0, 0,
             0, 0, 255, 0,
             0, 0, 0],

            [0, 0, 0,
             0, 255, 255, 0,
             0, 0, 255, 0, 0,
             0, 255, 255, 0,
             0, 0, 0],

            [0, 255, 0,
             0, 255, 255, 0,
             0, 0, 255, 0, 0,
             0, 255, 255, 0,
             0, 255, 0],

            [255, 255, 255,
             0, 255, 255, 0,
             0, 0, 255, 0, 0,
             0, 255, 255, 0,
             255, 255, 255],

            # [0, 255, 0,
            #  0, 255, 255, 0,
            #  0, 255, 255, 255, 0,
            #  0, 255, 255, 0,
            #  0, 255, 0],

            [255, 0, 0,
             0, 255, 0, 0,
             0, 0, 255, 0, 0,
             0, 0, 255, 0,
             0, 0, 255],
        ]
    },

    {
        'name': 'point',
        'meta': 'SENSOR_POINT',
        'centers_list': [

            [0, 0, 0,
             0, 0, 0, 0,
             0, 0, 255, 0, 0,
             0, 0, 0, 0,
             0, 0, 0]
        ]
    }
]