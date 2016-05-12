# file to read data from // TODO: move to argv system
import math

FILENAME = 'testfile.txt'

# metric to be chosen
METRIC_NUMBER = 0

metrics_list = [
    lambda x, y: math.sqrt(sum([(x.sensors[i] - y.sensors[i]) ** 2 for i in range(len(x.sensors))])),
]

# low edges to get inside Press
LOW_SENSOR_BORDER = 20
LOW_SENSOR_MISTAKE = 10

# count of SENSOR_INFO_SIZE to read by one attempt
DATA_CHUNK_SIZE = 100

# size of one sensor reading (in lines)
SENSOR_INFO_SIZE = 7

# sensor's ideal frames in each class
SENSOR_CIRCLE = [0, 0, 0,
                 0, 255, 255, 0,
                 0, 255, 0, 255, 0,
                 0, 255, 255, 0,
                 0, 0, 0]

SENSOR_LINE_STRICT = [0, 0, 0,
                      0, 255, 0, 0,
                      0, 0, 255, 0, 0,
                      0, 0, 255, 0,
                      0, 0, 0]

SENSOR_LINE_MISSED = [0, 0, 0,
                      0, 255, 255, 0,
                      0, 0, 255, 0, 0,
                      0, 255, 255, 0,
                      0, 0, 0]

SENSOR_POINT = [0, 0, 0,
                0, 0, 0, 0,
                0, 0, 255, 0, 0,
                0, 0, 0, 0,
                0, 0, 0]
