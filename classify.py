from collections import defaultdict

from data_classes import Frame, Shape
from settings import SENSOR_CLASSES, METRIC_NUMBER, METRICS_LIST, LOW_SENSOR_BORDER


def get_min_dist(frame, centers=None, rotate=False):
    """
    Calculates dists to centers and returns min value
    :param frame: frame to be classified (Frame)
    :param centers: list of ideal frame values (sensors) (list)
    :param rotate: should centers be rotated for better distances (boolean)
    :return: minimal distance to center
    """
    if centers is None:
        centers = [[0 for i in range(19)]]

    dists = []

    for center in centers:
        cent_fr = Frame(center)
        if rotate:
            for i in range(6):
                dists.append(METRICS_LIST[METRIC_NUMBER](frame, cent_fr))
                cent_fr.rotate_clock()
        else:
            dists.append(METRICS_LIST[METRIC_NUMBER](frame, cent_fr))

    return min(dists)


def get_dists(frame):
    """
    Detect types by expert system.
    Algorithm: get distances from frame to ideal centers (in each class) and get the shortest distance.
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
        frame.set_confidence(False)

    return frame.get_type()


def detect_press_type(press):
    """
    Detect press type by max frame classes
    :param press: Press object
    :return: detected press type
    """
    # TODO: detect by neighbours information
    for frame in press.frames:
        if frame.sensor_max > LOW_SENSOR_BORDER:
            frame_type = detect_frame_type(frame)
            press.class_counts[frame_type] += 1

            if not frame.is_confident():
                press.class_not_sure[frame_type] += 1

    press_class_info = []

    for sens_class, sens_class_count in press.class_counts.items():
        press_class_info.append(
            (
                sens_class,
                sens_class_count,
                press.class_not_sure[sens_class]
            )
        )

    press_class_info.sort(key=lambda x: (x[1], x[2], x[0]))
    final_type = press_class_info[-1]
    press.set_type(final_type[0])
    press.set_confidence(final_type[1] > 2*final_type[2])

    return press.get_type()
