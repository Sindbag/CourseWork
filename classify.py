from data_classes import Frame, Shape
from settings import SENSOR_CLASSES, METRIC_NUMBER, METRICS_LIST, LOW_SENSOR_BORDER, OFF_SCALE_COUNT,\
    FRAME_CONFIDENCE_PERCENT, PRESS_CONFIDENCE_PERCENT, OFF_SCALE_POINT


clusters = [Shape(row_sh) for row_sh in SENSOR_CLASSES]


def frame_valid(frame):
    """
    Frame validation function for more flexible frame selection
    :param frame: frame to classify
    :return: is frame valid? (boolean)
    """
    count = len([sens for sens in frame.sensors if sens >= OFF_SCALE_POINT])
    if OFF_SCALE_COUNT <= count and LOW_SENSOR_BORDER >= frame.sensor_max:
        return False
    return True


def get_min_dist(frame, centers=None, rotate=False):
    """
    Calculates dists to centers and returns min value
    :param frame: frame to be classified (Frame)
    :param centers: list of ideal frame values (sensors) (list)
    :param rotate: should centers be rotated for better distances (boolean)
    :return: minimal distance to center
    """
    if centers is None:
        centers = [Frame([0 for i in range(19)])]

    dists = []

    for cent_fr in centers:
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

    for shape in clusters:
        dists.append((shape.name, get_min_dist(frame, shape.center_frames, shape.rotate)))

    dists.sort(key=lambda x: x[1])
    return dists


def detect_frame_type(frame):
    dists = get_dists(frame)
    ans = dists[0]
    frame.set_type(ans[0])
    if len(dists) > 1 and dists[0][1] * (1.0 + float(FRAME_CONFIDENCE_PERCENT) / 100.0) > dists[1][1]:
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
        if frame_valid(frame):
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
    # print(press_class_info)

    final_type = press_class_info[-1]
    press.set_type(final_type[0])
    press.set_confidence((1.0 * final_type[1] * PRESS_CONFIDENCE_PERCENT / 100.0) > final_type[2])
    return press.get_type()
