import os
import sys

current_dir = os.path.dirname(__file__)
current_dir = os.path.normpath(current_dir)

template_path = os.path.join(current_dir, 'template.blend')
script_path = os.path.join(current_dir, 'process.py')

if sys.platform.startswith('linux'):
    blender_path = '/nwave/software/Blender/2.79a/linux64/blender'
else:
    blender_path = '//nwave/software/Blender/2.79a/win64/blender.exe'
