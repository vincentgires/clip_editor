import sys
import os

def normpath(path):
    
    # remove double slash to be able to use it in blender
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

