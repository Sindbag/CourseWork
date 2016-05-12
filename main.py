import os

from classify import expert_system_frame
from data_classes import Frame, Press
from settings import FILENAME, LOW_SENSOR_MISTAKE, LOW_SENSOR_BORDER, SENSOR_INFO_SIZE, DATA_CHUNK_SIZE


def read_data_part(f):
    output = []
    i = 0
    for i in range(SENSOR_INFO_SIZE * DATA_CHUNK_SIZE):
        l = f.readline()
        if (i % SENSOR_INFO_SIZE) == 0:
            if l.strip().split():
                num_list = list(map(int, l.strip().split()))
                output.append(Frame(num_list))
    return output


def minmax_of_frames(frames_list):
    """
    Get minimum of max frame's sensor's values
    :param frames_list: frames to get minmax from
    :return: minimum value of sensor_max of given frames
    """
    if not len(frames_list):
        raise Exception('Size of frames_list is 0')
    list_sens_min = frames_list[0].sensor_max
    for fr in frames_list:
        if fr.sensor_max < list_sens_min:
            list_sens_min = fr.sensor_max
    return list_sens_min


def read_presses(file):
    """
    Read data by chunks and assemble presses from it
    :param file: opened file to read from
    :return: presses list
    """
    presses_frame_list, presses = [], []
    in_press = False
    # read data, while not EOF(file)
    while file.tell() < os.fstat(file.fileno()).st_size:
        frames = read_data_part(file)
        last_frames = frames[:5]
        for fr in frames:
            # check if press is started
            if not in_press and minmax_of_frames(last_frames) > LOW_SENSOR_BORDER:
                presses_frame_list.append([])
                in_press = True
            if in_press:
                presses_frame_list[-1].append(fr)
                if minmax_of_frames(last_frames) < LOW_SENSOR_MISTAKE:
                    in_press = False
            del last_frames[0]
            last_frames.append(fr)
    for frame_list in presses_frame_list:
        presses.append(Press(frame_list))
    return presses


def main_program():
    f = open(FILENAME, 'r')
    presses = read_presses(f)
    for press in presses:
        # detect info about each frame in press and clarify type of press
        types_counter = [0, 0, 0, 0]  # 0 - none, 1 - line, 2 - circle, 3 - point
        for frame in press:
            # frame.detect_type()
            print(expert_system_frame(frame))
            # types_counter[frame.detect_type()] += 1


if __name__ == '__main__':
    main_program()
