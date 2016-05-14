import itertools


class Frame:
    """
    Data frame from sensor
    """
    new_id = itertools.count()

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
        self.detected_type = 'none'
        self.id = next(Frame.new_id)
        self.dists = [999999, 999999, 999999]
        self.is_sure = True

    def rotate_center_clock(self):
        tmp = self.sensors[4]
        self.sensors[4] = self.sensors[8]
        self.sensors[8] = self.sensors[13]
        self.sensors[13] = self.sensors[14]
        self.sensors[14] = self.sensors[10]
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

    def null_edges(self):
        frame_null_edges = [0, 0, 0,
                            0, 1, 1, 0,
                            0, 1, 1, 1, 0,
                            0, 1, 1, 0,
                            0, 0, 0]
        self.sensors = list(map(lambda x,y: x*y, self.sensors, frame_null_edges))

    def print_type(self):
        print(self.detected_type)

    def print_frame(self):
        print(*self.sensors[0:3], sep='\t', end='\n')
        print(*self.sensors[3:7], sep='\t', end='\n')
        print(*self.sensors[7:12], sep='\t', end='\n')
        print(*self.sensors[12:16], sep='\t', end='\n')
        print(*self.sensors[16:19], sep='\t', end='\n')

    def __str__(self):
        return str(self.print_frame()) + '\n' + str(self.print_type())

    def set_type(self, typename='none'):
        self.detected_type = typename
        return self.detected_type


class Press:
    """
    Class Press - list of frames + some information about it
    TODO: iterable on frames ?
    """
    def __init__(self, frames_list=None):
        if frames_list is None:
            frames_list = []
        self.frames = frames_list
        self.detected_type = 'none'
        self.is_sure = True
        self.start_frame = frames_list[0].id
        self.end_frame = frames_list[-1].id

    def max_contrast(self):
        max_cnt = max([x.sensor_max - x.sensor_min for x in self.frames])
        return filter(lambda x: (x.sensor_max - x.sensor_min == max_cnt), self.frames)


class Shape:
    """
    Objects with their ideal frames
    """
    def __init__(self, shape_info):
        self.name = shape_info['name']
        self.centers = shape_info['centers_list']
        # specific boolean to be sure in shape classification
        # self.specific

