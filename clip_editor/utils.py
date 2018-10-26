import sys
import os


def normpath(path):
    # remove double slash to be able to use it in Blender
    # result: /my/path
    if sys.platform.startswith('linux'):
        path = path.replace('//', '/')

    # make linux path compatible with windows
    # result after normpath: \\my\path
    elif sys.platform.startswith('win'):
        if path.startswith('/') and not path.startswith('//'):
            path = '/{}'.format(path)

    path = os.path.normpath(path)
    return path


def find_images(path):
    images = []
    dirname, basename = os.path.split(path)
    dirname = normpath(dirname)

    if '#' not in basename:
        return None

    length = 0
    index = basename.find('#')

    for i in basename[index:]:
        if i == '#':
            length += 1
        else:
            break

    for file in os.listdir(dirname):
        if len(file) == len(basename):
            check = True
            for i in range(length):
                if not file[index+i].isdigit():
                    check = False
            if check:
                images.append(file)

    images.sort()
    return images
