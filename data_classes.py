import itertools
from collections import defaultdict


class Frame:
    """
    Data frame from sensor
    """
    __new_id = itertools.count()
    __last_id = 0

    def __init__(self, sens_list=None):
        if sens_list is None:
            sens_list = [0 for i in range(19)]
        if len(sens_list) != 19:
            raise Exception('Wrong list length: ' + str(len(sens_list)) + ', expected 19')
        self.sensors = sens_list
        self.sensor_max = max(self.sensors)
        tmp = list(filter(lambda x: x > 0, self.sensors))
        if not tmp:
            self.sensor_min = 0
        else:
            self.sensor_min = min(tmp)
        self.__detected_type = 'none'
        # self._id = next(Frame.__new_id)
        self._id = Frame.__last_id
        Frame.__last_id += 1
        self.dists = []
        self._is_sure = True

    def __repr__(self):
        return 'f#{}'.format(self._id)

    @staticmethod
    def null_id():
        Frame.__last_id = 0

    def rotate_center_clock(self):
        tmp = self.sensors[4]
        self.sensors[4] = self.sensors[8]
        self.sensors[8] = self.sensors[13]
        self.sensors[13] = self.sensors[14]
        self.sensors[14] = self.sensors[10]
        self.sensors[10] = self.sensors[5]
        self.sensors[5] = tmp
        return self.sensors

    # TODO: rotate_counterclock
    # def rotate_center_counterclock(self):
    #     tmp = self.sensors[4]
    #     self.sensors[4] = self.sensors[5]
    #     self.sensors[5] = self.sensors[10]
    #     self.sensors[10] = self.sensors[14]
    #     self.sensors[14] = self.sensors[13]
    #     self.sensors[13] = self.sensors[8]
    #     self.sensors[8] = tmp

    def rotate_clock(self):
        self.rotate_center_clock()
        tmp = self.sensors[0]
        self.sensors[0] = self.sensors[3]
        self.sensors[3] = self.sensors[7]
        self.sensors[7] = self.sensors[12]
        self.sensors[12] = self.sensors[16]
        self.sensors[16] = self.sensors[17]
        self.sensors[17] = self.sensors[18]
        self.sensors[18] = self.sensors[15]
        self.sensors[15] = self.sensors[11]
        self.sensors[11] = self.sensors[6]
        self.sensors[6] = self.sensors[2]
        self.sensors[2] = self.sensors[1]
        self.sensors[1] = tmp
        return self.sensors

    def null_edges(self):
        frame_null_edges = [0, 0, 0,
                            0, 1, 1, 0,
                            0, 1, 1, 1, 0,
                            0, 1, 1, 0,
                            0, 0, 0]
        self.sensors = list(map(lambda x, y: x * y, self.sensors, frame_null_edges))
        return self.sensors

    def frame_str_format(self):
        return '\n'.join(
            [
                '\t'.join(list(map(str, self.sensors[0:3]))),
                '\t'.join(list(map(str, self.sensors[3:7]))),
                '\t'.join(list(map(str, self.sensors[7:12]))),
                '\t'.join(list(map(str, self.sensors[12:16]))),
                '\t'.join(list(map(str, self.sensors[16:19])))
            ]
        )

    def print_frame(self):
        print(self.frame_str_format(), end='\n')

    def print_type(self):
        print(self.__detected_type)
        return self.get_type()

    def get_type(self):
        return self.__detected_type

    def set_type(self, typename='none'):
        self.__detected_type = typename
        return self.__detected_type

    def is_confident(self):
        """
        Confidence in type detection
        :return: _is_sure property (boolean)
        """
        return self._is_sure

    def get_id(self):
        return self._id

    def __str__(self):
        return '\n'.join([
            'Frame #{}'.format(self.get_id()),
            'Type: {} , confident: {}'.format(self.get_type(), self.is_confident()),
            self.frame_str_format(),
        ])

    def set_confidence(self, sure=False):
        """
        Set _is_sure parameter (confidence in type detection)
        :param sure: boolean
        :return: new _is_sure value
        """
        self._is_sure = sure
        return self._is_sure


class Press:
    """
    List of frames + some information about it
    """

    def __init__(self, frames_list=None):
        if frames_list is None:
            frames_list = []
        self.frames = frames_list
        self.__detected_type = 'none'
        self._is_sure = True
        self.start_frame = min(fr.get_id() for fr in frames_list)
        self.end_frame = max(fr.get_id() for fr in frames_list)
        self.class_counts, self.class_not_sure = defaultdict(int), defaultdict(int)

    def max_contrast_frames(self):
        max_cnt = max([x.sensor_max - x.sensor_min for x in self.frames])
        return filter(lambda x: (x.sensor_max - x.sensor_min == max_cnt), self.frames)

    def is_confident(self):
        return self._is_sure

    def set_confidence(self, sure=False):
        """
        Set _is_sure value (confidence in type detection)
        :param sure: boolean
        :return: new _is_sure value
        """
        self._is_sure = sure
        return self._is_sure

    def get_type(self):
        return self.__detected_type

    def set_type(self, typename='none'):
        self.__detected_type = typename
        return self.get_type()

    def __str__(self):
        return 'Frames range: {} - {}\n' \
               'Press type: {}\n' \
               'Is confident: {}'.format(
                    self.start_frame,
                    self.end_frame,
                    self.get_type(),
                    self.is_confident()
               )

    def __repr__(self):
        return 'Pr#({}-{})'.format(self.start_frame, self.end_frame)


class Shape:
    """
    Objects with their ideal frames
    """
    def __init__(self, shape_info):
        self.name = shape_info['name']
        self.centers = shape_info['centers_list']
        self.rotate = shape_info.get('rotate', False)

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name
