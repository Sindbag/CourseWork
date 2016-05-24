# default file to read data from
FILENAME = 'input.txt'

# count of SENSOR_INFO_SIZE to read by one attempt
DATA_CHUNK_SIZE = 300

# size of one sensor data reading (in lines)
SENSOR_INFO_SIZE = 7

# metric to be chosen
METRIC_NUMBER = 0
METRIC_POWER = 19

# list of functions take 2 arguments (x, y) - frames, vector is frame.sensors
METRICS_LIST = [
    lambda x, y: float(pow(sum(abs(x.sensors[i] - y.sensors[i]) ** METRIC_POWER for i in range(len(x.sensors))),
                           1.0 / METRIC_POWER)),
    lambda x, y: min([abs(x.sensors[i] - y.sensors[i]) for i in range(len(x.sensors))]),
    lambda x, y: max([abs(x.sensors[i] - y.sensors[i]) for i in range(len(x.sensors))])
]

# percent of dists difference to be confident in classification
FRAME_CONFIDENCE_PERCENT = 30
# percent of non-confident frames in press for non-confident press classification
PRESS_CONFIDENCE_PERCENT = 30

# range to check sensors value to start and end Press
FRAMES_START_PRESS = 20
FRAMES_STOP_PRESS = 40

# max sensors value to start Press
LOW_SENSOR_BORDER = 50

# max sensors value to stop Press
LOW_SENSOR_MISTAKE = 20

# count of sensors to verify frame as overshoot
OFF_SCALE_COUNT = 9
OFF_SCALE_POINT = 250

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
        'rotate': True,
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

            [255, 0, 0,
             0, 255, 0, 0,
             0, 0, 255, 0, 0,
             0, 0, 255, 0,
             0, 0, 255],

            [255, 255, 255,
             0, 255, 255, 0,
             0, 0, 255, 0, 0,
             0, 255, 255, 0,
             255, 255, 255],

            # [0, 200, 0,
            #  0, 230, 230, 0,
            #  0, 200, 255, 200, 0,
            #  0, 230, 230, 0,
            #  0, 200, 0],
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
    },
]
