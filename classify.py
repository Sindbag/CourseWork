import math
from data_classes import Frame, FrameType
from settings import SENSOR_POINT, SENSOR_CIRCLE, METRIC_NUMBER, SENSOR_LINE_STRICT, SENSOR_LINE_MISSED

metrics_list = [
    lambda x, y: math.sqrt(sum([(x.sensors[i] - y.sensors[i]) ** 2 for i in range(len(x.sensors))])),
]


def expert_system_frame(frame):
    """
    Detect types by expert system.
    Algorithm: get distances from self-frame to ideal frames (in each class) and get the shortest distance.
    :param frame: sensor's data frame to be classified
    :return: dict of minimal distances to frame-classes' centers
    """
    ideal_point, ideal_circle = Frame(SENSOR_POINT), Frame(SENSOR_CIRCLE)

    dist_point_center = metrics_list[METRIC_NUMBER](frame, ideal_point)
    dist_circle_center = metrics_list[METRIC_NUMBER](frame, ideal_circle)

    strict_ideal_line, missed_ideal_line = Frame(SENSOR_LINE_STRICT), Frame(SENSOR_LINE_MISSED)
    dists_strict_line_centers, dists_missed_line_centers = [], []

    for i in range(4):
        dists_strict_line_centers.append(metrics_list[METRIC_NUMBER](frame, strict_ideal_line))
        strict_ideal_line.rotate_center_clock()

        dists_missed_line_centers.append(metrics_list[METRIC_NUMBER](frame, missed_ideal_line))
        missed_ideal_line.rotate_center_clock()

    min_dist_strict_line = min(dists_strict_line_centers)
    min_dist_missed_line = min(dists_missed_line_centers)

    dists = {
        'point': dist_point_center,
        'circle': dist_circle_center,
        'strict_line': min_dist_strict_line,
        'missed_line': min_dist_missed_line
    }

    # print(frame.print_frame())
    # print(dists)
    return dists


def detect_frame_type(frame):
    dists = expert_system_frame(frame)
    minimum = dists.values()[0]
    ans = ()
    for (x, y) in dists:
        if y < minimum:
            ans = (x, y)
            minimum = y
    # TODO : clarify class
    if ans[0] == 'point':
        frame_type = 3
    elif ans[0] == 'circle':
        frame_type = 2
    else:
        frame_type = 1
    frame.set_type(frame_type)
    return FrameType(ans[0])


def expert_system_press(press):
    pass


def detect_press_type(press):
    pass
