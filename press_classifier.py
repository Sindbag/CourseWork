import os
import sys

from classify import detect_press_type
from data_classes import Frame
from file_operations import read_presses
from settings import FILENAME


def process_press(presses=None):
    if not presses:
        print('No frames detected')
        return
    for press in presses:
        # detect info about each press
        print(
            'Frames range: {} - {}\n'
            'Press type: {}\n'
            'Is confident: {}'.format(
                press.start_frame,
                press.end_frame,
                detect_press_type(press),
                press.is_confident(),
            ),
            end='\n\n'
        )


def file_proceed(f):
    if not f.endswith('.txt'):
        print('{0} file is not supported (.txt expected)'.format(f))
    Frame.null_id()
    file = open(f, 'r')
    presses = read_presses(file)
    print('File: {}\n'.format(f))
    process_press(presses)


def main_program():
    if len(sys.argv) > 1:
        for file in sys.argv[1:]:
            if os.path.isdir(file):
                for f in [os.path.join(file, x) for x in os.listdir(file) if os.path.isfile(os.path.join(file, x))]:
                    file_proceed(f)
            else:
                file_proceed(file)
    else:
        file_proceed(FILENAME)


if __name__ == '__main__':
    main_program()
