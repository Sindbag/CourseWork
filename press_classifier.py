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


def main_program():
    if len(sys.argv) > 1:
        for file in sys.argv[1:]:
            Frame.null_id()
            f = open(file, 'r')
            presses = read_presses(f)
            print('File: {}\n'.format(file))
            process_press(presses)
    else:
        f = open(FILENAME, 'r')
        presses = read_presses(f)
        process_press(presses)


if __name__ == '__main__':
    main_program()
