from data_classes import Frame, Shape
from settings import SENSOR_CLASSES, METRIC_NUMBER, metrics_list, LOW_SENSOR_BORDER


def get_min_dist(frame, centers=None, rotate=False):
    if centers is None:
        centers = [[0 for i in range(19)]]

    dists = []

    for center in centers:
        cent_fr = Frame(center)
        if rotate:
            for i in range(6):
                dists.append(metrics_list[METRIC_NUMBER](frame, cent_fr))
                cent_fr.rotate_clock()
        else:
            dists.append(metrics_list[METRIC_NUMBER](frame, cent_fr))

    return min(dists)


def get_dists(frame):
    """
    Detect types by expert system.
    Algorithm: get distances from self-frame to ideal frames (in each class) and get the shortest distance.
    :param frame: sensor's data frame to be classified
    :return: sorted list of tuples (class, dist) of minimal distances to frame-classes' centers
    """
    dists = []

    for shape_raw in SENSOR_CLASSES:
        shape = Shape(shape_raw)
        dists.append((shape.name, get_min_dist(frame, shape.centers)))

    dists.sort(key=lambda x: x[1])
    return dists


def detect_frame_type(frame):
    dists = get_dists(frame)
    ans = dists[0]
    frame.set_type(ans[0])

    if dists[0][1]*1.2 > dists[1][1]:
        frame.is_sure = False

    return frame.detected_type


def detect_press_type(press):
    """
    Detect press type by max frame classes
    :param press: Press object
    :return: detected press type
    """
    press.class_counts, press.class_not_sure = {}, {}
    # previous_type = 'none'
    for frame in press.frames:
        if frame.sensor_max > LOW_SENSOR_BORDER:
            frame_type = detect_frame_type(frame)
            press.class_counts[frame_type] = \
                press.class_counts.get(frame_type, 0) + 1

            if not frame.is_sure:
                press.class_not_sure[frame_type] = \
                    press.class_not_sure.get(frame_type, 0) + 1
            # previous_type = frame.detected_type
    press_class_info = []

    for sens_class, class_count in press.class_counts.items():
        press_class_info.append((sens_class, class_count, press.class_not_sure.get(sens_class, 0)))

    press_class_info.sort(key=lambda x: (x[1], x[2], x[0]))

    press.detected_type = press_class_info[-1][0]

    return press.detected_type
