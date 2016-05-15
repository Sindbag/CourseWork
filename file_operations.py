import os
from data_classes import Frame, Press
from settings import LOW_SENSOR_MISTAKE, LOW_SENSOR_BORDER, SENSOR_INFO_SIZE, DATA_CHUNK_SIZE, \
    FRAMES_START_PRESS, FRAMES_STOP_PRESS


def eof(file):
    return file.tell() >= os.fstat(file.fileno()).st_size


def read_data_part(file):
    """
    Read file and get frames from sensor's data
    :param file: file to be read
    :return: frames list
    """
    frames = []
    for i in range(SENSOR_INFO_SIZE * DATA_CHUNK_SIZE):
        l = file.readline()
        if eof(file):
            return frames
        if (i % SENSOR_INFO_SIZE) == 0:
            if l.strip().split():
                num_list = list(map(int, l.strip().split()))
                frames.append(Frame(num_list))
    return frames


def is_press_ended(frames_list=None):
    """
    :param frames_list: frames to check
    :return: is press ended? (boolean)
    """
    if frames_list is None:
        frames_list = []
    max_sens = max([fr.sensor_max for fr in frames_list[-FRAMES_STOP_PRESS:]])
    return max_sens < LOW_SENSOR_MISTAKE


def is_press_started(frames_list=None):
    """
    :param frames_list: frames to check
    :return: is press started? (boolean)
    """
    if frames_list is None:
        frames_list = []
    min_sens = min([fr.sensor_max for fr in frames_list[-FRAMES_START_PRESS:]])
    return min_sens > LOW_SENSOR_BORDER


def read_presses(file):
    """
    Read data by chunks and assemble presses from it
    :param file: opened file to read from
    :return: presses list
    """
    presses_frame_list = []
    in_press = False
    # read data, while not EOF(file)
    last_frames = [Frame() for i in range(max(FRAMES_START_PRESS, FRAMES_STOP_PRESS))]
    while not eof(file):
        frames = read_data_part(file)
        for fr in frames:
            last_frames = list(last_frames[1:])
            last_frames.append(fr)

            # check if press started
            if not in_press and is_press_started(last_frames):
                new_list = list(last_frames)
                presses_frame_list.append(new_list)
                in_press = True

            # check if press ended
            if in_press:
                presses_frame_list[-1].append(fr)
                if is_press_ended(last_frames):
                    in_press = False
    presses = []
    for frame_list in presses_frame_list:
        presses.append(Press(frame_list))
    return presses


def read_all_frames(file):
    frame_list = []
    while not eof(file):
        frame_list.extend(read_data_part(file))
    return frame_list
