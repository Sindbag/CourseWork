from data_classes import Frame
from settings import SENSOR_POINT, SENSOR_CIRCLE, METRIC_NUMBER, SENSOR_LINE_STRICT, SENSOR_LINE_MISSED, metrics_list


def expert_system_frame(frame):
    """
    Detect types by expert system.
    Algorithm: get distances from self-frame to ideal frames (in each class) and get the shortest distance.
    :param frame: sensor's data frame to be classified
    :return: sorted list of tuples (class, dist) of minimal distances to frame-classes' centers
    """
    point, circle = Frame(SENSOR_POINT), Frame(SENSOR_CIRCLE)

    dist_point, dist_circle = map(lambda x: metrics_list[METRIC_NUMBER](frame, x), [point, circle])

    strict_line, missed_line = Frame(SENSOR_LINE_STRICT), Frame(SENSOR_LINE_MISSED)
    dists_strict_line, dists_missed_line = [], []

    for i in range(4):
        dists_strict_line.append(metrics_list[METRIC_NUMBER](frame, strict_line))
        strict_line.rotate_center_clock()

        dists_missed_line.append(metrics_list[METRIC_NUMBER](frame, missed_line))
        missed_line.rotate_center_clock()

    min_dist_strict_line, min_dist_missed_line = map(min, [dists_strict_line, dists_missed_line])

    dists = [
        ('point', dist_point),
        ('circle', dist_circle),
        ('strict_line', min_dist_strict_line),
        ('missed_line', min_dist_missed_line)
    ]
    dists.sort(key=lambda x: x[1])
    return dists


def detect_frame_type(frame):
    dists = expert_system_frame(frame)
    ans = dists[0]
    # TODO : clarify class
    not_sure = False
    if ans[0] == 'point':
        if not frame.sensor_max == frame.sensors[10]:
            not_sure = True
        frame_type = 3
    elif ans[0] == 'circle':
        if not (frame.sensors[10] < frame.sensors[5] and
                frame.sensors[10] < frame.sensors[6] and
                frame.sensors[10] < frame.sensors[9] and
                frame.sensors[10] < frame.sensors[11] and
                frame.sensors[10] < frame.sensors[14] and
                frame.sensors[10] < frame.sensors[15]):
            not_sure = True
        frame_type = 2
    else:
        frame_type = 1
    frame.set_type(frame_type)
    return frame_type


def expert_system_press(press):
    pass


def detect_press_type(press):
    pass
