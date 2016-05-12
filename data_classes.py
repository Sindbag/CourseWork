from enum import Enum
import itertools


class FrameType(Enum):
    none = 0
    line = 1
    circle = 2
    point = 3


class Frame:
    """
    Кадр данных, считанный с сенсора
    """
    new_id = itertools.count()

    def __init__(self, sens_list=None):
        if sens_list is None:
            sens_list = [0 for i in range(19)]
        if len(sens_list) != 19:
            raise Exception('Wrong list length: ' + str(len(sens_list)) + ', expected 19')
        self.sensors = sens_list
        self.sensor_max = max(self.sensors)
        self.sensor_min = min(filter(lambda x: x > 0, self.sensors))
        self.detected_type = 0
        self.id = next(Frame.new_id)

    def rotate_center_clock(self):
        tmp = self.sensors[4]
        self.sensors[4] = self.sensors[8]
        self.sensors[8] = self.sensors[13]
        self.sensors[14] = self.sensors[14]
        self.sensors[15] = self.sensors[10]
        self.sensors[10] = self.sensors[5]
        self.sensors[5] = tmp

    def rotate_center_counterclock(self):
        tmp = self.sensors[4]
        self.sensors[4] = self.sensors[5]
        self.sensors[5] = self.sensors[10]
        self.sensors[10] = self.sensors[14]
        self.sensors[14] = self.sensors[13]
        self.sensors[13] = self.sensors[8]
        self.sensors[8] = tmp

    def print_type(self):
        print(FrameType(self.detected_type))

    def print_frame(self):
        print(*self.sensors[0:3], sep='\t', end='\n')
        print(*self.sensors[3:7], sep='\t', end='\n')
        print(*self.sensors[7:12], sep='\t', end='\n')
        print(*self.sensors[12:16], sep='\t', end='\n')
        print(*self.sensors[16:19], sep='\t', end='\n')

    def __str__(self):
        return str(self.print_frame()) + '\n' + str(self.print_type())

    def set_type(self, typenum=0):
        if not 0 <= typenum <= 3:
            raise Exception('Wrong type number: ' + str(typenum) + ', expected 0-3')
        self.detected_type = typenum
        return self.detected_type


class Press:
    """
    Class Press - list of frames + some information about it
    TODO: iterable on frames
    """
    def __init__(self, frames_list=None):
        if frames_list is None:
            frames_list = []
        self.frames = frames_list

    def max_contrast(self):
        max_cnt = max([x.sensor_max - x.sensor_min for x in self.frames])
        return filter(lambda x: (x.sensor_max - x.sensor_min == max_cnt), self.frames)
